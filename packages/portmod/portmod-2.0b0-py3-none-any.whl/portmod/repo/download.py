# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from typing import AbstractSet, Iterable, List, Optional

import urllib
import urllib.request
import urllib.error
import urllib.parse
import requests
import os
from progressbar import ProgressBar, Percentage, Bar, ETA, FileTransferSpeed

from portmod.repo.util import get_hash
from portmod.globals import env
from ..config import get_config
from ..pybuild import FullPybuild, Hash, Pybuild, Source
from ..repos import get_repo
from .metadata import get_license_groups, get_repo_root
from .usestr import use_reduce
from .use import get_use


def parse_arrow(sourcelist: Iterable[str]) -> List[Source]:
    """
    Turns a list of urls using arrow notation into a list of
    Source objects
    """
    result: List[Source] = []
    arrow = False
    for value in sourcelist:
        if arrow:
            result[-1] = Source(result[-1].url, value)
            arrow = False
        elif value == "->":
            arrow = True
        else:
            url = urllib.parse.urlparse(value)
            result.append(Source(value, os.path.basename(url.path)))
    return result


def get_filename(basename: str) -> str:
    """
    Returns the location of the local cached version of the source file
    corresponding to the given name. The file may or may not exist.
    @return the cache location of the given source name
    """
    return os.path.join(env.DOWNLOAD_DIR, basename)


def mirrorable(mod: Pybuild, enabled_use: Optional[AbstractSet[str]] = None) -> bool:
    """
    Retuerns whether or not a mod can be mirrored
    """
    # FIXME: Determine which sources have use requirements
    # that don't enable mirror or fetch
    if "mirror" not in mod.RESTRICT and "fetch" not in mod.RESTRICT:
        redis: Iterable[str]
        if mod.INSTALLED:
            redis = get_license_groups(get_repo(mod.REPO).location).get(
                "REDISTRIBUTABLE", []
            )
        else:
            redis = get_license_groups(get_repo_root(mod.FILE)).get(
                "REDISTRIBUTABLE", []
            )

        def is_license_redis(group):
            if isinstance(group, str):
                return group in redis
            elif group[0] == "||":
                return any(is_license_redis(li) for li in group)
            else:
                return all(is_license_redis(li) for li in group)

        if enabled_use and is_license_redis(
            use_reduce(mod.LICENSE, enabled_use, opconvert=True)
        ):
            return True
        if not enabled_use and is_license_redis(
            use_reduce(mod.LICENSE, opconvert=True, matchall=True)
        ):
            return True

    return False


def fetchable(mod: FullPybuild) -> List[Source]:
    """
    Returns the list of fetchable sources associated with a mod
    A source can be fetched if it is mirrorable,
    or if it has a URI
    """
    if "fetch" in mod.RESTRICT:
        return []

    use, _ = get_use(mod)
    if "mirror" not in mod.RESTRICT and mirrorable(mod, use):
        return mod.get_default_sources()

    can_fetch = []
    for source in mod.get_default_sources():
        parsedurl = urllib.parse.urlparse(source.url)
        if parsedurl.scheme:
            can_fetch.append(source)

    return can_fetch


def download(url: str, dest_name: str, *, size: Optional[int] = None):
    """
    Downloads the given url to the path specified by dest_name
    Raises exceptions as defined by urllib.request.urlretrieve
    """
    print("Fetching {}".format(url))

    os.makedirs(env.DOWNLOAD_DIR, exist_ok=True)

    req = requests.get(url, stream=True)
    if "Content-Length" in req.headers:
        remote_size = int(req.headers["Content-Length"].strip())
    else:
        remote_size = None
    numbytes = 0
    bar = ProgressBar(
        widgets=[Percentage(), " ", Bar(), " ", ETA(), " ", FileTransferSpeed()],
        redirect_stdout=True,
        max_value=remote_size or size,
    ).start()
    with open(get_filename(dest_name), mode="wb") as file:
        for buf in req.iter_content(1024):
            if buf:
                file.write(buf)
                numbytes += len(buf)
                bar.update(numbytes)
    bar.finish()


def check_hash(filename: str, hashes: Iterable[Hash]) -> bool:
    """
    Returns true if and only if the sha512sum of the given file
    matches the given checksum
    """
    for h in hashes:
        return bool(get_hash(filename, h.alg.func) == h.value)
    return False


def get_download(name: str, hashes: Optional[Iterable[Hash]]) -> Optional[str]:
    """
    Determines if the given file is in the cache.
    The file must match both name and checksum
    @return path to donloaded file
    """
    if os.path.exists(get_filename(name)) and (
        hashes is None or check_hash(get_filename(name), hashes)
    ):
        return get_filename(name)

    # If a file with spaces otherwise matches, remove the spaces
    if os.path.exists(env.DOWNLOAD_DIR):
        for file in os.listdir(env.DOWNLOAD_DIR):
            src = get_filename(file)
            if file.replace(" ", "_") == name and (
                hashes is None or check_hash(src, hashes)
            ):
                dest = get_filename(name)
                os.rename(src, dest)
                return dest

    return None


def is_downloaded(mod: FullPybuild) -> bool:
    """
    Returns true if the mod's sources are all present in the cache
    """
    for source in mod.get_default_sources():
        cached = get_download(source.name, source.hashes)
        if cached is None:
            return False
    return True


def download_source(mod, source: Source, check: bool = True) -> str:
    """
    Downloads the given source file.
    @return the path to the downloaded source file
    """
    if check:
        cached = get_download(source.name, source.hashes)
    else:
        cached = get_download(source.name, None)
    fetch = "fetch" not in mod.get_restrict()
    mirror = (
        "mirror" not in mod.get_restrict()
        and "fetch" not in mod.get_restrict()
        and mirrorable(mod)
    )

    if cached:
        # Download is in cache. Nothing to do.
        return cached
    elif not fetch:
        # Mod cannot be fetched and is not already in cache. abort.
        raise Exception("Source {} not in cache and cannot be fetched".format(source))
    else:
        parsedurl = urllib.parse.urlparse(source.url)

        # Download archive
        filename = get_filename(source.name)

        if mirror:
            PORTMOD_MIRRORS = get_config()["PORTMOD_MIRRORS"].split()
            for mirror_url in PORTMOD_MIRRORS:
                url = urllib.parse.urljoin(mirror_url, source.name)
                try:
                    download(url, source.name, size=source.size)
                except urllib.error.HTTPError as e:
                    print(f"Unable to fetch {url}: {e}")
                    continue

                if check and not check_hash(filename, source.hashes):
                    raise Exception(
                        "Source file {} has invalid checksum!".format(source.name)
                    )

                return filename

        if parsedurl.scheme != "":
            download(source.url, source.name, size=source.size)
            if check and not check_hash(filename, source.hashes):
                raise Exception(
                    "Source file {} has invalid checksum!".format(source.name)
                )
            return filename

        raise Exception("Unable to download {}".format(source.url))


def download_mod(mod: FullPybuild, matchall=False) -> List[Source]:
    """
    Downloads missing sources for the given mod in its current USE configuration
    @return A list of paths of the sources for the mod
    """
    download_list = []
    if matchall:
        sources = mod.get_sources(matchall=True)
    else:
        sources = mod.get_default_sources()

    for source in sources:
        download_source(mod, source)

        download_list.append(source)

    return download_list
