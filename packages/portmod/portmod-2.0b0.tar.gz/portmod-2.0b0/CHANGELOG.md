# Changelog

## [2.0_beta0] 2020-04-02

### Dependencies
- Development versions of Portmod require setuptools_scm at runtime for fetching
  version information.
- All versions require python-sat
- Python 3.7 64-bit or 3.8 64-bit is required on Windows, as these are the only
  pre-built wheels available for python-sat. Additionally, python-sat must be
  version 0.1.5.dev4.
- Microsoft Visual C++ Redistributable is required on Windows (necessary for
  python-sat pre-compiled wheels).
- Portmod will now make use of the libyaml backend of PyYAML if it is available
  (see https://pyyaml.org/wiki/LibYAML )

### User Features

#### Added
- Comments (beginning with #) are now supported in mod.use, mod.accepts_keywords
  and similar files.
- Local archive files can now be passed on the command line to omwmerge.
  These files will be moved to the cache directory, and portmod will install the
  mods they correspond to.

#### Changed
- Portmod will now handle dependencies more intelligently and display conflicts
  more verbosely. Most use flag changes that are required to avoid conflicts will
  now be detected automatically.
- Portmod now caches pybuilds to speed up most operations significantly.
- The config will now only be sorted at the end of mod installation, or as needed
  when a build file accesses the VFS.

### Pybuild/Dev Features

#### Changed
- Pybuild files should now import from `pybuild` module rather than
  `portmod.pybuild`. The current behaviour will be supported at least until
  v2.0
- Portmod now uses thin manifests that only contain DIST entries. As such, you
  now only need to run `pybuild file.pybuild manifest` when a pybuilds source
  archives have changed.
- Repositories now declare their master repositories in the file
  `metadata/layout.conf`. This file uses the same format as other python-like
  config files, and masters should be a whitespace-delimited string list of
  repository names. E.g. `masters = "openmw openmw-testing"`
- The DESC field is now reflowed such that newlines are replaced by spaces. I.e.
  you can add newlines to maintain proper line length, without affecting how
  they are displayed in search results (note that descriptions longer than one
  line are discouraged).
- AA (list of all mod sources) Has been removed. It was not used and was deprecated
  in eapi 7 (see PMS).
- File.MASTERS (alias of File.OVERRIDES) has been removed.
- Manifest files now only store entries for DIST files.

#### Added
- The beginnings of a stable interface is now being provided via the root
  portmod module (now that it is no longer part of the pybuild import tree).
  These functions will be maintained between major versions of portmod such
  that any dependent software/scripts does not break when portmod updates.
- Field values in field-based config entries are now stringified. Practically,
  this means you can now use integers as values when specifying config information
  in pybuild fields such as FALLBACK.
- File and InstallDir objects now are stringified in a manner similar to how they are
  created. E.g. `InstallDir("path", REQUIRED_USE="foo")`
- hasattr and getattr can now be used inside pybuilds.
- Added UNFETCHED variable to pass sources that need to be fetched to mod_nofetch
  function.
- File.OVERRIDES can now be a list of files (makes it possible to handle files
  containing spaces). Old functionality of being a string that can contain use
  conditionals has been maintained.
- Added the builtins of next, iter, filter, map, max, min, dict, enumerate, sum,
  any, all, reversed and sorted to the sandbox
- Blockers can now be included in the DATA_OVERRIDES fields to indicate underridden
  mods.

### Bugfixes
- Fixed fetching portmod version information for development versions (i.e.
  when there is no installed python egg info).
- Fixed a bug which may cause sorting mods to report cycles incorrectly due to
  the code attempting to trace cycles via empty nodes.
- Fixed some bugs in how use flags are displayed for mods, caused by empty lists
  (e.g. when no flags are enabled) being treated the same as the special case of
  None.
- Fixed bug where portmod would interrupt downloads directly into the cache for
  files that contain spaces by renaming the file prior to it having finished
  downloading.
- Exceptions will no longer be raised if a mod's installation does not exist
  when a mod is removed (e.g. due to a previous error).
- Read-only files will be removed properly when uninstalling mods and cleaning up
  the temporary directories during installation.
- The portmod.conf placeholder file will always be created when portmod is invoked.
  previously it would not prior to profile selection.
- Fixed error when displaying licenses the user needs to accept.
- Portmod will no longer throw exceptions when initializing with a version of
  GitPython less than 3.0.5.
- Fixed issue where we were failing to download files from the gitlab-based file mirror.
- Pybuild files can no longer install to arbitrary paths by using chains of `..` in
  PATCHDIR to escape the build directory.

## [2.0_alpha6] - 2020-01-28

Note that one of the bugfixes changed the data directory produced by
base/morrowind. If you previously had this installed, you will need to
manually remove the old data entry from openmw.cfg (`omwmerge --sort` will
produce a warning about the line).

### Dependencies
- Windows now requires [Sandboxie](https://www.sandboxie.com/).
- All platforms now require [RedBaron](https://github.com/PyCQA/redbaron)

### User Features
- Windows: Replaced SANDBOX_COMMAND with automatic sandboxie configuration.
- Added `--nodeps` argument, which can be used to ignore dependencies when
  installing. Note that this is designed for debugging purposes, and may
  cause mods to fail to install, or fail to work if their dependencies are
  missing.

### Pybuild/Dev Features
- Added support for raising errors when stderr is printed to in the sandboxed
  execute function
- Added support for in-place variables to the sandbox. I.e. +=, -= type
  operations can now be used in Pybuilds.
- Added _unpack_sequence_ to sandbox. I.e. `a, b = "baz".split("a")` now works
  in the sandbox
- portmod.query.query now optionally takes multiple fields, and outputs as a
  generator function
- Added list_dir function for scanning for vfs files
- Added utility functions to Pybuilds for getting enabled Files and InstallDirs

### Bugfixes
- Added requirement that RestrictedPython be >= 4.0 to setup.py.
  This had been previously documented, but not enforced.
- Replaced configparser with redbaron to fix automatic modifications to user
  config. This had been broken since the introduction of the python-based
  config file
- fixed display of USE_EXPAND type flags in searches and transaction list
- Fixed how omwcmd dependency is handled in CI to ensure we aren't spending
  unnecessary time re-building it.
- Fixed Windows path issue where profile path would be malformed
- Fixed Windows bug where mod could not be uninstalled due to attempting to
  remove the current working directory.
- Fixed bug where we were replacing spaces with underscores in fallback section
  values, in addition to the keys and section names (where it's necessary).
  Fallback entries now match what is produced by the openmw-iniimporter
- Made symlinks be resolved when producing path to include in config files.
  This means that the data entry in openmw.cfg generated by base/morrowind will
  now match the one generated by the openmw-wizard, meaning that, with the
  previous bugfix, the wizard will no longer cause problems if run before portmod.
- Made sure that we create parent directories for config files if they do not exist.
- We no longer block module imports for the pyclass module, as it is entirely
  sandboxed. This was done since the code for blocking modules requires running
  the module outside of the sandbox, code indended for use with system modules which
  are trusted, not untrusted modules like pyclass.
- Setuptools now enforces the need for RestrictedPython>=4.0 via setup.py
- Repo name parsing in Atoms now matches the PMS, and doesn't consume USE flag conditions
  if both are provided.

## [2.0_alpha5] - 2019-12-24

Small release, primarily to fix a significant bug introduced in previous version.

### User Features
- Made display of included source directories be unambigous (previously relative
  directory paths were shown, but not which archive they came from if there are
  multiple archives).

### Bugfixes
- Fixed bug that would prevent mods with `RESTRICT="fetch"` from being installed.
  Introduced by changes to fetchability detection in v2.0_alpha4.

## [2.0_alpha4] - 2019-12-23

Biggest release yet, largely since it's long overdue.

### Windows Support
After support for Windows having lapsed after the introduction of the sandbox,
various Windows bugs have now been resolved, Windows CI has been introduced, and
it *should* mostly work now.

Two issues are outstanding:
- Executable sandboxes are still shaky. Theoretically, [sandboxie](https://www.sandboxie.com/),
  which is now free, and soon to be open-source, could be used. Currently adoption
  is limited by its current EULA preventing any sort of installation in the CI
  environment. Users are welcome to try and get it to work, providing the
  appropriate `SANDBOX_COMMAND`, otherwise, Portmod will now inform you of
  commands that are being attempted (so you can check that they're benign)
  and prompt you to allow them to run without a sandbox.
- There is an unknown bug showing up in CI where files are unable to be deleted
  due to "being used by another process".

### User features
- Added support for [user config sorting rules](https://gitlab.com/portmod/portmod/-/wikis/Configuration/User-Sorting-Rules).
- Cycle detection when doing dependency resolution and sorting the config is now
  more verbose
- Added support for no-argument depclean (i.e. `omwmerge --depclean`) to remove
  mods that were pulled in as dependencies but are no longer needed. They can be
  removed automatically using the `--auto-depclean` or `-x` flag when performing
  other operations.
- Added `OMWMERGE_DEFAULT_OPTS` environment variable to allow the use of default
  options that are always passed to `omwmerge`. `--ignore-default-opts` can be used
  to override this.
- Windows users will be prompted if they have not set `SANDBOX_COMMAND` and install
  a mod that requires external executable calls.
- Housekeeping operations (sorting, updating the VDB, etc.), are now performed even
  if mods fail to install.
- We now track when the config needs to be sorted, and if necessary will retry
  sorting even if no other operations need to be performed.

### Pybuild/Dev features
- The `pwinreg` module has been added, providing a read_reg function for reading
  values from the Windows registry, as well as `HKEY_` constants from `winreg`.
- The "fetch" and "mirror" `RESTRICT` values are no longer recommended to be used
  in Pybuilds, as new smarter behaviour detects if mods can be fetched or mirrored
  using the mod's license and uri.
- `src_unpack` can now be used for manual unpacking of mods. To assist this, an
  `unpack` function has also been added.

### Bugfixes
- Mods only available in the installed DB can now be re-installed (also fixed in
  last release... This time for sure!)
- Fixed how we remove entries that use indices (the `i` variable) in ini-type
  config files.
- The downgrade transaction is now used where appropriate.
- The config path is now properly expanded when accessing the VFS.
- Various names (not used) which are not available on win32 have been removed from
  the sandboxed os module.
- Sandbox now has access to `/run` and `/etc`, which is necessary for git calls.
- Display of maintainers in search results has been cleaned up, and no longer
  throws an exception if there are multiple maintainers.
- USE_EXPAND has been fixed, and now behaves like it does in Portage.
- When removing test directories (which may contain read-only files that cannot
  be otherwise removed on Windows), we now give write access to files that fail
  to be deleted, before retrying.
- Added an extra layer of backslashes to backslashes on Windows in files handled
  by the sandbox (unknown why this is necessary).
- Added workaround for upstream python Windows Pathlib bug (https://bugs.python.org/issue38671)
- Removed shlex for subprocess calls on Windows, as they are not needed and
  cause errors on Windows.
- Cleaned up how we handle trailing junk in mod directory paths so that they
  are normalized in a cross-platform way.
- Default values for user.name and user.email are now provided for the git
  repository in the VDB (note that this repo is for internal use, so these
  values don't need to be correct).
- Config sorting is now performed after each mod is installed (instead of
  once at the end) to ensure that it always reflects the current state of
  the installation, since it may be used by mods for VFS lookups.
- The FileNotFoundError exception is now provided by the sandbox.
- Fixed bug when comparing versions of an installed mod with an updated version.

## [2.0_alpha3] - 2019-09-08

### Dependency changes
- Now requires omwcmd 0.2
- `dcv` is no longer a dependency (undocumented requirement of the
  `openmw-conflicts` executable)

### User Features
- `omwmerge --info` now only displays a useful subset of config variables.
  Full set can be viewed by also passing `--verbose`.

### Pybuild/Dev Features
- `InstallDir.SOURCE` has been deprecated in favour of `InstallDir.S`, which
  refers to the extracted archive name (without extension).
- USE_EXPAND support. Notably allowing nice localization support through the
  L10N config variable.
- Inquisitor will no longer allow mods names that end in a version component,
  which are invalid as they cannot be properly parsed.

### Bugfixes
- Fixed bug in detecting which files we can detect masters from that meant we
  previously were ignoring masters for all files.
- Fixed handling of environment variables to override config variables.
- Fixed depcleaning mods that include blockers (`!!`).
- Made updates be shown as update transactions rather than new mods even if the
  update option is not passed.
- Fixed reinstalling mods from DB if mod is no longer available.
- Mods with revision numbers (E.g. `cat/foo-1.0-r1`) no longer cause an exception
  to be thrown when encountered.

## [2.0_alpha2]- 2019-08-11
### Bugfixes
- Fixes second setuptools_scm issue.

## [2.0_alpha1] - 2019-08-10

### Bugfixes
- Fixed incorrect Download link on Pypi and issue with the Portmod update
  detection mechanism (which warns if a repository is marked as using a newer
  version of Portmod than is currently installed).

## [2.0_alpha0] - 2019-08-10

First Alpha release of Portmod 2.0
