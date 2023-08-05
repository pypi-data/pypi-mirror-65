# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Dependency resolution module

Converts mod dependency links and REQUIRED_USE conditions into a MAX-SAT formula in
conjunctive normal form.
This formula is then solved using pysat (python-sat on pypi) and the resulting model
converted back into a list of installed mods and their use flag configuration.

Note that the hard requirements defined in DEPEND, RDEPEND and REQUIRED_USE are
converted into a SAT formula that must be solved in its entirety.
We use a MAX-SAT solver because there are also other soft requirements which are used
to avoid installing mods unnecessarily and to avoid changing the user's use flag
configuration, if possible.

See https://en.wikipedia.org/wiki/Boolean_satisfiability_problem for details on
the SAT problem
"""

import copy
import re
from functools import cmp_to_key
from types import SimpleNamespace
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple, Union

from pysat.examples.rc2 import RC2
from pysat.formula import WCNFPlus
from pysat.solvers import Solver

from ..colour import blue, green
from ..pybuild import Pybuild
from ..transactions import ModDoesNotExist, Transactions, UseDep, generate_transactions
from .atom import Atom, FQAtom, QualifiedAtom, atom_sat, version_gt
from .loader import load_all_installed, load_installed_mod, load_mod, load_mod_fq
from .sets import get_set, is_selected
from .use import get_user_global_use, get_user_use, get_forced_use, get_use
from .usestr import human_readable_required_use, parse_usestr
from .util import get_keyword_dep


class AmbigiousAtom(Exception):
    """Indicates that multiple mods from different categories match"""


class DepError(Exception):
    """Indicates an unsatisfiable transaction"""


def token_conflicts(token1: str, token2: str) -> bool:
    """
    Returns true if and only if two tokens, which use minus-format (e.g. -foo)
    to indicate a disabled token, conflict. E.g. foo and -foo
    """
    return (
        token1.lstrip("-") == token2.lstrip("-")
        and token1[0] == "-"
        and token2[0] != "-"
        or token1[0] != "-"
        and token2[0] == "-"
    )


def negate(token: str) -> str:
    """Returns the negation of the given token"""
    if token.startswith("-"):
        return token.lstrip("-")
    return "-" + token


class Formula:
    """
    Intermediate representation of the integer WCNFPlus SAT formula accepted by pysat

    All flags are disabled by prepending a "-"

    Atom requirements are represented by the fully qualified atom,
    as produced by mod.ATOM

    Use flag requirements are represented by the fully qualified atom
    of the mod they apply to, followed by [flag]

    Custom variables are prefixed by an underscore and are
    used only for the calculation and ignored in the output
    """

    __i = 1  # Integer counter, for the numerical equivalent of tokens
    __j = 1  # Variable name counter.
    __numcache: Dict[str, int] = {}  # Strings are
    __stringcache: Dict[int, str] = {}
    __variabledesc: Dict[str, str] = {}

    class Clause:
        """Generic clause type"""

        def __init__(self, clause: Iterable[str]):
            self.requirements: Set[str] = set()
            self.clause = clause
            self.intclause: Optional[Iterable[int]] = None

        def str2num(self):
            """
            Converts the tokens in the clause to integers for use with pysat
            """
            result = copy.copy(self)
            result.intclause = list(map(Formula.getnum, self.clause))
            return result

        def sourceatom(self) -> Optional[Atom]:
            return None

    class MetaClause(Clause):
        def __init__(
            self,
            source: Optional[str],
            desc: Optional[str],
            clause: Iterable[str],
            weight: Optional[int],
            atmost: Optional[int],
        ):
            self.source = source
            self.desc = desc
            self.clause = clause
            self.weight = weight
            self.atmost = atmost
            self.requirements: Set[str] = set()

        def __str__(self):
            return f"{self.source} - {self.desc}"

        def sourceatom(self) -> Optional[Atom]:
            if isinstance(self.source, Atom):
                return self.source
            return None

    class DepClause(Clause):
        def __init__(self, source: str, clause: Iterable[str], dependency: Atom):
            super().__init__(clause)
            self.source = source
            self.dependency = dependency

        def __str__(self):
            return f"{green(self.dependency)}: required by {green(self.source)}"

        def blocks(self, model: Set[str], clause: "Formula.MetaClause") -> bool:
            if isinstance(clause, Formula.BlockerClause):
                if atom_sat(self.dependency, clause.blocked) and all(
                    req in model for req in self.requirements
                ):
                    return True

            return False

        def sourceatom(self) -> Optional[Atom]:
            if isinstance(self.source, Atom):
                return self.source
            return None

    class BlockerClause(Clause):
        def __init__(self, source: str, clause: Iterable[str], blocked: Atom):
            super().__init__(clause)
            self.source = source
            self.blocked = blocked

        def __str__(self):
            return f"{green(self.blocked)}: blocked by {green(self.source)}"

        def blocks(self, model: Set[str], clause: "Formula.MetaClause") -> bool:
            if isinstance(clause, Formula.DepClause):
                if atom_sat(self.blocked, clause.dependency) and all(
                    req in model for req in self.requirements
                ):
                    return True

            return False

        def sourceatom(self) -> Optional[Atom]:
            if isinstance(self.source, Atom):
                return self.source
            return None

    class UseDepClause(Clause):
        def __init__(self, atom: Atom, clause: Iterable[str], depatom: Atom, flag: str):
            super().__init__(clause)
            self.atom = self.source = atom
            self.depatom = depatom
            self.flag = flag

        def __str__(self):
            return f"{green(self.depatom)}[{self.flag}]: required by {green(self.atom)}"

        def blocks(self, model: Set[str], clause: "Formula.MetaClause") -> bool:
            if isinstance(clause, Formula.UseDepClause):
                if (
                    atom_sat(self.depatom, clause.depatom)
                    and token_conflicts(self.flag, clause.flag)
                    and all(req in model for req in self.requirements)
                ):
                    return True
            elif isinstance(clause, Formula.RequiredUseClause):
                if (
                    atom_sat(clause.atom, self.depatom)
                    and token_conflicts(self.flag, clause.flag)
                    and all(req in model for req in self.requirements)
                ):
                    return True

            return False

        def sourceatom(self) -> Optional[Atom]:
            return self.atom

    class RequiredUseClause(Clause):
        def __init__(
            self,
            atom: Atom,
            clause: Iterable[str],
            flag: str,
            tokens: List[Union[str, List]],
        ):
            super().__init__(clause)
            self.atom = self.source = atom
            self.flag = flag
            self.tokens = tokens

        def __str__(self):
            if self.flag.startswith("__"):  # If flag is a generated variable
                string = Formula.get_variable_desc(self.flag)
            else:
                if self.flag[0] == "-":
                    string = "-" + list(Atom(self.flag[1:]).USE)[0]
                else:
                    string = list(Atom(self.flag).USE)[0]
            return (
                f"{green(self.atom)} could not satisfy {blue(string)}, which is part of"
                f"the larger clause {blue(human_readable_required_use(self.tokens))}"
            )

        def blocks(self, model: Set[str], clause: "Formula.MetaClause") -> bool:
            if isinstance(clause, Formula.UseDepClause):
                if (
                    atom_sat(self.atom, clause.depatom)
                    and token_conflicts(self.flag, clause.flag)
                    and all(req in model for req in self.requirements)
                ):
                    return True
            elif isinstance(clause, Formula.RequiredUseClause):
                if (
                    atom_sat(self.atom, clause.atom)
                    and token_conflicts(self.flag, clause.flag)
                    and all(req in model for req in self.requirements)
                ):
                    return True

            return False

        def sourceatom(self) -> Optional[Atom]:
            return self.atom

    def __init__(self):
        self.clauses = []
        self.atoms: Dict[QualifiedAtom, Set[FQAtom]] = {}
        self.flags = set()

    @classmethod
    def getnum(cls, string: str) -> int:
        if string in cls.__numcache:
            return cls.__numcache[string]

        if string[0] == "-":
            cls.__numcache[string] = -cls.__i
            cls.__numcache[string[1:]] = cls.__i
            cls.__stringcache[-cls.__i] = string
            cls.__stringcache[cls.__i] = string[1:]
        else:
            cls.__numcache[string] = cls.__i
            cls.__numcache["-" + string] = -cls.__i
            cls.__stringcache[cls.__i] = string
            cls.__stringcache[-cls.__i] = "-" + string

        cls.__i += 1
        return cls.__numcache[string]

    @classmethod
    def getstring(cls, num: int) -> str:
        return cls.__stringcache[num]

    @classmethod
    def genvariable(cls, desc: List[Any]) -> str:
        var = "__" + str(cls.__j)
        cls.__j += 1
        cls.__variabledesc[var] = human_readable_required_use(desc)
        return var

    @classmethod
    def get_variable_desc(cls, var: str) -> str:
        return cls.__variabledesc[var]

    def merge(self, other: "Formula"):
        self.clauses.extend(other.clauses)
        for clause in other.clauses:
            self.__update_for_clause__(clause.clause)
        return self

    def get_wcnfplus(self) -> WCNFPlus:
        formula = WCNFPlus()
        for clause in self.get_clauses():
            if isinstance(clause, Formula.MetaClause) and clause.weight is not None:
                formula.append(clause.intclause, weight=clause.weight)
            elif isinstance(clause, Formula.MetaClause) and clause.atmost is not None:
                formula.append([clause.intclause, clause.atmost], is_atmost=True)
            else:
                formula.append(clause.intclause)
        return formula

    def append(
        self,
        clause: Iterable[str],
        from_atom: Optional[str] = None,
        desc: Optional[str] = None,
        weight=None,
        atmost=None,
    ):
        self.clauses.append(Formula.MetaClause(from_atom, desc, clause, weight, atmost))
        self.__update_for_clause__(clause)

    def append_dep(self, clause: Iterable[str], from_atom: str, dependency: Atom):
        self.clauses.append(Formula.DepClause(from_atom, clause, dependency))
        self.__update_for_clause__(clause)

    def append_blocker(self, clause: Iterable[str], from_atom: str, blocked: Atom):
        self.clauses.append(Formula.BlockerClause(from_atom, clause, blocked))
        self.__update_for_clause__(clause)

    def append_required_use(
        self,
        clause: Iterable[str],
        from_atom: Atom,
        flag: str,
        tokens: List[Union[str, List]],
    ):
        self.clauses.append(Formula.RequiredUseClause(from_atom, clause, flag, tokens))
        self.__update_for_clause__(clause)

    def append_usedep(
        self, clause: Iterable[str], from_atom: Atom, dep_atom: Atom, flag: str
    ):
        self.clauses.append(Formula.UseDepClause(from_atom, clause, dep_atom, flag))
        self.__update_for_clause__(clause)

    def __update_for_clause__(self, clause: Iterable[str]):
        for token in clause:
            if not token.startswith("_") and not token.startswith("-_"):
                if "[" not in token:
                    atom = FQAtom(token.lstrip("-"))
                    if atom.CMN in self.atoms:
                        self.atoms[QualifiedAtom(atom.CMN)].add(atom)
                    else:
                        self.atoms[QualifiedAtom(atom.CMN)] = {atom}
                else:
                    self.flags.add(token.lstrip("-"))

    def extend(
        self,
        from_atom: Atom,
        clauses: List[List[str]],
        desc: Optional[str] = None,
        weight=None,
        atmost=None,
    ):
        for clause in clauses:
            self.append(clause, from_atom, desc, weight, atmost)

    def add_constraints(self, constraints: List[str]):
        self.__update_for_clause__(constraints)
        for clause in self.clauses:
            if not (
                isinstance(clause, Formula.MetaClause) and clause.atmost is not None
            ):
                clause.clause = list(clause.clause) + constraints
                clause.requirements |= {negate(token) for token in constraints}

    def get_clauses(self):
        for clause in self.clauses:
            yield clause.str2num()


def get_atmost_one_formulae(tokens: Sequence[str]) -> List[List[str]]:
    """
    Returns a list of clauses that enforce that at most one of the tokens may be true

    Note that this can also be achieved by using Formula.append with atmost set to 1,
    however  this does not provide a mechanism for handling additional conditions.
    Instead, you can use this function, and add the condition to each clause it produces
    """
    if len(tokens) <= 1:
        return []

    result = []
    # Enforce that for any two tokens in the list, one must be false
    for token in tokens[1:]:
        # Invert value of firsttoken
        if tokens[0].startswith("-"):
            firsttoken = tokens[0].lstrip("-")
        else:
            firsttoken = "-" + tokens[0]

        # Invert value of the other token
        if token.startswith("-"):
            othertoken = token.lstrip("-")
        else:
            othertoken = "-" + token
        result.append([firsttoken, othertoken])

    return result + get_atmost_one_formulae(tokens[1:])


def get_required_use_formula(mod: Pybuild, tokens: List[Union[str, List]]) -> Formula:
    """
    Adds clauses to the given formula for the given mod's REQUIRED_USE

    :param tokens: List of tokens corresponding to the REQUIRED_USE string, parsed
            beforehand by parse_usestr to be a list of tokens, with sublists
            corresponding to brackets in the original string
    """

    def get_required_use_formula_inner(
        tokens: List[Union[str, List]]
    ) -> Tuple[Formula, List[str]]:
        formula = Formula()
        clausevars = []

        for token in tokens:
            if isinstance(token, list):
                if token[0] != "??" and token[0].endswith("?"):
                    newvar = Formula.genvariable([token])
                    subformulae, subvars = get_required_use_formula_inner(token[1:])
                    if token[0].startswith("!"):
                        usedep = mod.ATOM + "[" + token[0].lstrip("!").rstrip("?") + "]"
                        subformulae.add_constraints([usedep, "-" + newvar])
                    else:
                        usedep = "-" + mod.ATOM + "[" + token[0].rstrip("?") + "]"
                        subformulae.add_constraints([usedep, "-" + newvar])
                    # for clause in get_atmost_one_formulae(subvars):
                    #    formula.append_required_use(
                    #        ["-" + newvar] + clause, mod.ATOM, token
                    #    )
                    formula.merge(subformulae)
                    # Generated variable is added to clausevars, and is free if
                    # condition is unsatisfied, and matches subformulae if condition
                    # is satisfied
                    clausevars.append(newvar)
                else:
                    subformulae, subvars = get_required_use_formula_inner(token[1:])
                    newvar = Formula.genvariable([token])
                    # Note: newvar will only have the value False if the formula
                    # is satisfied
                    if token[0] in ("??", "^^"):
                        for clause in get_atmost_one_formulae(subvars):
                            formula.append(
                                ["-" + newvar] + clause,
                                mod.ATOM,
                                human_readable_required_use(tokens),
                            )
                    if token[0] in ("||", "^^"):
                        formula.append(
                            ["-" + newvar] + subvars,
                            mod.ATOM,
                            human_readable_required_use(tokens),
                        )
                    if token[0] in ("||", "^^", "??"):
                        # If clause is satisfied, and the operator is not AND,
                        # then the subclauses don't need to be all satisfied
                        subformulae.add_constraints([newvar])
                    formula.merge(subformulae)
                    clausevars.append(newvar)

            else:
                var = mod.ATOM + "[" + token.lstrip("!") + "]"
                if token.startswith("!"):
                    formula.append_required_use(
                        ["-" + var], mod.ATOM, "-" + var, tokens
                    )
                    clausevars.append("-" + var)
                else:
                    formula.append_required_use([var], mod.ATOM, var, tokens)
                    clausevars.append(var)
        return formula, clausevars

    formula, clausevars = get_required_use_formula_inner(tokens)
    # Top level is an and, so require that all returned variables are satisfied
    for var in clausevars:
        formula.append_required_use([var], mod.ATOM, var, tokens)
    return formula


def get_dep_formula(mod: Pybuild, tokens) -> Tuple[Formula, Set[FQAtom]]:
    """
    Adds clauses to the given formula for the dependency strings of the given mod

    :param tokens: List of tokens corresponding to the dependency string, parsed
            beforehand by parse_usestr to be a list of tokens, with sublists
            corresponding to brackets in the original string
    """

    def fstr(atom: Atom, flag: str) -> str:
        return atom + "[" + flag.rstrip("?=").lstrip("!-") + "]"

    def flagstr(atom: Atom, flag: str) -> str:
        disabled = flag.startswith("!")
        flag = flag.rstrip("?").lstrip("!")
        # Note: If flag was disabled, we want the flag enabled in the clause, as it
        # should either be enabled,
        # or some other part of the clause must be true if disabled
        if disabled:
            return fstr(atom, flag)
        # Note: If flag was enabled, we produce the clause (flag => dep),
        # which is equivalent to (-flag | dep)
        return "-" + fstr(atom, flag)

    formula = Formula()
    deps: Set[FQAtom] = set()

    for token in tokens:
        if isinstance(token, list) and token[0] == "||":
            # If token is an or, next token is a list, at least one of the elements of
            # which must be satisfied
            orvars = []

            # Create clause for each part of the || expression.
            for subclause in token[1:]:
                # Create new variable to represent clause
                var = Formula.genvariable([token])
                orvars.append(var)
                # Either one part of the or must be true, or the variable for
                # the clause should be false
                new_formula, new_deps = get_dep_formula(mod, [subclause])
                new_formula.add_constraints(["-" + var])
                formula.merge(new_formula)
                deps |= new_deps

            # We should be able to set at least one of the new variables we
            # introduced to be true, meaning that some other part of their clause
            # must be satisfied
            formula.append(orvars, mod.ATOM, human_readable_required_use([token]))
        elif isinstance(token, list) and token[0].endswith("?"):
            new_formula, new_deps = get_dep_formula(mod, token[1:])
            new_formula.add_constraints([flagstr(mod.ATOM, token[0])])
            formula.merge(new_formula)
            deps |= new_deps
        elif token.startswith("!!"):
            for _mod in load_mod(Atom(token.lstrip("!"))):
                formula.append_blocker(
                    ["-" + _mod.ATOM], mod.ATOM, Atom(token.lstrip("!"))
                )
                deps.add(_mod.ATOM)

        # Handle regular dependencies, ignoring virtual system atoms
        elif not Atom(token).C or not Atom(token).startswith("sys-"):
            atom = Atom(token)

            # Note that load_mod will only return mods that completely match atom
            # I.e. it will handle any versioned atoms itself
            specificatoms = [m.ATOM for m in load_mod(atom)]

            deps |= set(specificatoms)

            # At least one specific version of this mod must be enabled
            formula.append_dep(specificatoms, mod.ATOM, atom)

            # For each use flag dependency, add a requirement that the flag must be set
            # This depends on the operators used on the flag. See PMS 8.2.6.4
            for flag in atom.USE:
                for spec_atom in specificatoms:
                    # Either specific version should not be installed,
                    # or flag must be set (depending on flag operators)

                    # Use requirement is unnecessary unless this specific version
                    # of the mod is enabled
                    new_formula = Formula()

                    if flag.startswith("-"):  # dep[-flag]
                        # 2-style disabled
                        new_formula.append_usedep(
                            ["-" + flagstr(spec_atom, flag)], mod.ATOM, atom, flag
                        )
                    elif flag.endswith("="):  # dep[flag=] or dep[!flag=]
                        # 4-style enabled/disabled if and only if enabled/disabled
                        # for parent mod

                        if flag.startswith("!"):
                            # If !flag=, then flag for dep should be disabled if flag
                            # for mod is enabled
                            prefix = "-"
                            nprefix = ""
                        else:
                            # Otherwise, they should be equal
                            prefix = ""
                            nprefix = "-"

                        var = Formula.genvariable([f"{spec_atom}[{flag}]"])

                        new_formula.extend(
                            mod.ATOM,
                            [
                                # Both must be enabled if var is disabled
                                [var, prefix + fstr(spec_atom, flag)],
                                [var, fstr(mod.ATOM, flag)],
                                # Both must be disabled if var is enabled
                                ["-" + var, nprefix + fstr(spec_atom, flag)],
                                ["-" + var, "-" + fstr(mod.ATOM, flag)],
                            ],
                        )

                        # Since var must be either enabled or disabled, either both must
                        # be enabled, or both must be disabled
                    elif flag.endswith("?"):
                        # 4-style enabled/disabled if (but not only if) enabled/disabled
                        # for parent mod
                        if flag.startswith("!"):  # dep[!flag?]
                            # Either flag must be enabled for mod,
                            # or disabled for dependency
                            new_formula.append_usedep(
                                [fstr(mod.ATOM, flag), "-" + fstr(spec_atom, flag)],
                                mod.ATOM,
                                spec_atom,
                                flag,
                            )
                        else:  # dep[flag?]
                            # Either flag must be disabled for mod,
                            # or enabled for dependency
                            new_formula.append_usedep(
                                ["-" + fstr(mod.ATOM, flag), fstr(spec_atom, flag)],
                                mod.ATOM,
                                spec_atom,
                                flag,
                            )
                    else:  # dep[flag]
                        # 2-style enabled
                        new_formula.append_usedep(
                            [fstr(spec_atom, flag)], mod.ATOM, spec_atom, flag
                        )

                    new_formula.add_constraints(["-" + spec_atom])
                    formula.merge(new_formula)
    return formula, deps


def resolve(
    selected: Iterable[Atom],
    deselected: Iterable[Atom],
    *,
    deep: bool = False,
    update: bool = False,
    newuse: bool = False,
    noreplace: bool = False,
    depclean: bool = False,
    prefer_installed: bool = True,
) -> Transactions:
    """
    Calculates new mod configuration to match system after the given mods are installed

    Note: We have two modes of operation.
    1. Shallow - We assume that all installed mods are fixed and will not
        change version. Any version of a newly selected mods may be installed.
        Note that use flags may change on installed mods.
    2. Deep - We treat every mod as newly selected, and choose from among its versions
    """

    print("Calculating Dependencies...")
    formula = Formula()

    # List of sets of mod objects, with each being a specific version of that mod
    oldselected = []
    newselected = dict()

    CMD_ATOM = "mods passed on command line"
    WORLD_ATOM = "world favourites file"

    for atom in list(selected) + list(deselected):
        if not load_mod(atom):
            raise ModDoesNotExist("Unable to find mod for atom {}".format(atom))

    if deep:
        # All selected mods are considered new. All deps are pulled in fresh
        newselectedset = {atom: CMD_ATOM for atom in selected}
        newselectedset.update({atom: WORLD_ATOM for atom in get_set("world")})
        for atom in deselected:
            name = load_mod(atom)[0].CMN
            if name in newselectedset:
                del newselectedset[name]
        oldselectedset = set()
    elif depclean:
        oldselectedset = get_set("world") - {
            load_mod(atom)[0].CMN for atom in deselected
        }
        newselectedset = {atom: CMD_ATOM for atom in selected}
    else:
        oldselectedset = {mod.CMN for mod in load_all_installed(flat=True)} - {
            load_installed_mod(atom).CMN for atom in deselected
        }
        newselectedset = {atom: CMD_ATOM for atom in selected}

    for atom in deselected:
        for mod in load_mod(atom):
            formula.append_dep(["-" + mod.ATOM], CMD_ATOM, atom)

    def create_modlist(atom):
        modset = set(load_mod(atom))

        installed_mod = load_installed_mod(atom)
        if installed_mod:
            modset.add(installed_mod)

        modlist = list(modset)

        # Raise exception if mod name is ambiguous (exists in multiple categories)
        if not all(mod.ATOM.C == modlist[0].ATOM.C for mod in modlist):
            raise AmbigiousAtom(
                f"Atom {green(atom)} is ambiguous and could refer to any of "
                "the following: \n  "
                + green("\n  ".join(sorted([mod.ATOM for mod in modlist])))
            )

        if not modlist:
            if atom in set(selected):
                raise ModDoesNotExist(f"Cannot find mod to satisfy mod {atom}")
            else:
                raise ModDoesNotExist(
                    f"Cannot find mod to satisfy mod {atom} in world file"
                )
        return modlist

    newselectedatoms: Set[Atom] = set()
    for atom, source in newselectedset.items():
        modlist = create_modlist(atom)
        name = modlist[0].CMN
        if name in newselected:
            newselected[modlist[0].CMN][0].extend(modlist)
            if newselected[modlist[0].CMN][2] is CMD_ATOM or source is CMD_ATOM:
                # Use generic atom if included multiple times on command line.
                # Not all versions in modlist will correspond to a specific version
                # passed on the command line.
                newselected[modlist[0].CMN][1] = name
            # Prefer command line as source rather than world file
            if newselected[modlist[0].CMN][2] is WORLD_ATOM and source is CMD_ATOM:
                newselected[modlist[0].CMN][2] = CMD_ATOM
        else:
            newselected[modlist[0].CMN] = [modlist, atom, source]
        newselectedatoms.add(QualifiedAtom(modlist[0].CMN))

    for atom in oldselectedset:
        if atom not in newselectedatoms:
            modlist = create_modlist(atom)
            oldselected.append((modlist, atom, "world favourites file"))

    # Mods where we've added their deps to the formula
    depsadded: Set[FQAtom] = set()
    # Queue of mods to add to the formula
    new: List[Pybuild] = []
    # Ensure newselected and oldselected mods are satisfied
    for modlist, sourceatom, source in list(newselected.values()) + oldselected:
        # At least one version of the mod must be installed
        formula.append_dep([mod.ATOM for mod in modlist], source, sourceatom)
        new += modlist

    while new:
        # Mods to parse in next iteration, mapped to the mod that depends on them
        nextmods: Set[FQAtom] = set()
        for mod in new:
            # Either mod must not be installed, or mods dependencies must be satisfied
            new_formula, deps = get_dep_formula(
                mod, parse_usestr(mod.DEPEND + " " + mod.RDEPEND)
            )
            new_formula.merge(
                get_required_use_formula(mod, parse_usestr(mod.REQUIRED_USE))
            )
            new_formula.add_constraints([f"-{mod.ATOM}"])
            formula.merge(new_formula)
            for flag in get_forced_use(mod.ATOM):
                if flag[0] == "-":
                    formula.append(
                        [f"-{mod.ATOM}[{flag[1:]}]"],
                        "use.force",
                        "Forced flag from profile",
                    )
                else:
                    formula.append(
                        [f"{mod.ATOM}[{flag}]"], "use.force", "Forced flag from profile"
                    )

            depsadded.add(mod.ATOM)
            # Add this mod's dependencies to the next set of mods to parse
            nextmods |= deps
        new = []
        for atom in nextmods:
            if atom not in depsadded:
                new.append(load_mod_fq(atom))

    # Soft clauses to minimize unwanted changes to user's configuration

    # Clause for each version, with newest version (no keyword change) having the
    #  highest weight
    #  Followed by other versions without keyword changes
    #  Then versions requiring keyword changes in order of version
    #  Then versions requiring unmasking in order of version
    # Note: the largest of these must be smaller than the base weight of not having the
    # mod installed

    # Track maximum update weight so that we can make sure that higher-priority clauses
    # always have a greater weight, even if they have many version
    max_up_weight = 0

    weights = SimpleNamespace()

    ###################################################################################
    weights.base_update = 1  # Base weight for the lowest
    weights.update_diff = 10  # Difference between each update, in order
    # Weight added to versions which are installed
    # Negative for now, as there are still some issues installing mods from db
    # TODO: There might be advantages to preferring re-installing from db
    # such as avoiding re-downloading files just because the sources changed in a trivial
    # manner
    weights.installed_preference = prefer_installed * -1
    weights.user_flag = 3  # Weight to keep a user-set flag the same
    weights.default_flag = 2  # Weight to keep a flag at its default value
    # Weight to keep mods that are installed, but not selected
    # The negative of this is set if depclean is enabled (plus max_up_weight)
    weights.keep_installed = 1
    ###################################################################################
    # The following also have the max_up_weight added to them, to ensure they always
    # weigh more than the weights given to mod versions
    ###################################################################################
    # To keep specific versions of installed mods that have not been selected this
    # run installed
    weights.oldselected = 1000
    # Weight to keep a mod that is not selected and not installed disabled
    weights.not_needed = 1
    ###################################################################################

    for group in formula.atoms:
        # Divide mods into stable, testing and unstable
        # If user accepts testing keywords, they will be considered stable
        stable = set()
        testing = set()
        unstable = set()
        for atom in formula.atoms[group]:
            mod = load_mod_fq(atom)
            keyword = get_keyword_dep(mod)
            if not keyword:
                stable.add(atom)
            elif keyword.keyword.startswith("~"):
                testing.add(atom)
            elif keyword.keyword == "**":
                unstable.add(atom)

            def cmp(x, y):
                if version_gt(x.MVR, y.MVR):
                    return 1
                return -1

        i = weights.base_update
        inc = 10

        def weigh(li):
            nonlocal i
            for atom in sorted(li, key=cmp_to_key(cmp)):
                if atom.endswith("::installed "):
                    # Prefer installed version if available.
                    # Remote version may contain packaging changes
                    # that require downloading new versions of the source files
                    formula.append([atom], weight=i + 1)
                else:
                    formula.append([atom], weight=i)
                i += inc

        weigh(unstable)
        weigh(testing)
        weigh(stable)
        if i > max_up_weight:
            max_up_weight = i + 1

        # At most one oversion of the mod must be installed
        formula.append(
            formula.atoms[group],
            "inviolable-rule",
            "At most one version may be installed",
            atmost=1,
        )

    # For oldselected mods the highest weight is given to the already installed version
    # We shouldn't try to update these
    for modlist, _, _ in oldselected:
        for mod in modlist:
            if mod.INSTALLED:
                formula.append([mod.ATOM], weight=weights.oldselected + max_up_weight)

    # Clause for each mod installed, but not selected, with a small weight
    #    to keep them installed
    # If depclean is set, we instead weigh them to remove if possible
    for mod in load_all_installed(flat=True):
        if not is_selected(mod.ATOM) and not Atom(mod.CMN) in newselectedatoms:
            if depclean:
                formula.append(
                    ["-" + mod.ATOM], weight=weights.keep_installed + max_up_weight
                )
            else:
                formula.append([mod.ATOM], weight=weights.keep_installed)

    # Clause for each mod not installed, with a small weight to keep them not installed
    for group in formula.atoms:
        for atom in formula.atoms[group]:
            if (
                not load_installed_mod(Atom(atom.CMN))
                and not is_selected(atom)
                and not Atom(atom.CMN) in newselectedatoms
            ):
                formula.append(["-" + atom], weight=weights.not_needed + max_up_weight)

    # Clause for each use flag, with a small weight for the default setting,
    #    and a large weight for the user's configuration (if any)
    for flagatom in formula.flags:
        parsed = Atom(flagatom)
        flag = list(parsed.USE)[0]  # Note: each only has one flag
        disabledflag = "-" + flag
        enabledatom = flagatom.lstrip("-")
        disabledatom = "-" + enabledatom
        atom_nouse = Atom(parsed.split(f"[{flag}]")[0].lstrip("-"))
        modlist = load_mod(atom_nouse)
        if modlist:
            assert len(modlist) == 1
            mod = modlist[0]
        else:
            mod = load_installed_mod(atom_nouse)
            if not mod:
                raise Exception(Atom(atom_nouse))

        user_flags = get_user_use(mod.ATOM)
        global_user_flags = get_user_global_use()
        if flag in user_flags:
            formula.append([enabledatom], weight=weights.user_flag)
        elif disabledflag in user_flags:
            formula.append([disabledatom], weight=weights.user_flag)
        elif flag in global_user_flags:
            formula.append([enabledatom], weight=weights.user_flag)
        elif disabledflag in global_user_flags:
            formula.append([disabledatom], weight=weights.user_flag)
        elif flag in get_use(mod)[0]:  # default value
            formula.append([enabledatom], weight=weights.default_flag)
        else:
            formula.append([disabledatom], weight=weights.default_flag)

    wcnf = formula.get_wcnfplus()
    solver = RC2(wcnf, solver="mc")
    solver.compute()
    if solver.compute():
        print("Done!")
        # Turn numbers in result back into strings
        result = list(
            filter(
                # Filter out custom variables that are only meaningful
                # for the computation
                lambda x: not x.startswith("_") and not x.startswith("-_"),
                [Formula.getstring(num) for num in solver.model],
            )
        )
        flags = [atom for atom in result if "[" in atom]
        enabled = [FQAtom(mod) for mod in result if "[" not in mod and mod[0] != "-"]
        enablednames = [atom.CMN for atom in enabled]
        disabled = [
            FQAtom(mod.lstrip("-"))
            for mod in result
            if "[" not in mod and mod[0] == "-"
            # If mod is enabled and installed version is disabled,
            # ignore disabled version, and vice versa
            and Atom(mod.lstrip("-")).CMN not in enablednames
        ]
        usedeps = []

        for flag in flags:
            atom = FQAtom(flag.lstrip("-"))
            if flag[0] == "-":
                prefix = "-"
            else:
                prefix = ""

            # Ignore flags for mods that are to be uninstalled
            if re.sub(r"\[.*\]", "", atom) in enabled:
                usedeps.append(UseDep(Atom(atom.CM), prefix + list(atom.USE)[0], None))

        transactions = generate_transactions(
            enabled,
            disabled,
            newselectedatoms,
            usedeps,
            noreplace=noreplace,
            update=update,
            newuse=newuse,
            delete=bool(deselected or depclean),
        )
        return transactions

    # Find clause that caused the solver to fail
    # Backtrack mod that added that clause until we reach @selected by
    # looking for clauses containing the (enabled) mod as a token.
    # Display this trace.
    # Then also display trace for a mod that requires/blocks the clause that
    # caused the failure

    solver2 = Solver("mc")
    solveableformula = []
    # Add atmost clauses first, as they won't by themselves cause conflicts,
    # and are not very useful for explaining a failed transaction
    for clause in formula.get_clauses():
        if isinstance(clause, Formula.MetaClause) and clause.atmost is not None:
            solver2.add_atmost(clause.intclause, clause.atmost)

    model = set()
    for clause in formula.get_clauses():
        if isinstance(clause, Formula.MetaClause) and (
            clause.atmost is not None or clause.weight is not None
        ):
            continue
        else:
            solver2.add_clause(clause.intclause)

        if solver2.solve():
            model = set(map(Formula.getstring, solver2.get_model()))
            solveableformula.append(clause)
        else:
            conflict = None

            for solveableclause in solveableformula:
                # Find clause that contradicts failed clause
                # Note that metaclauses don't have a blocks function,
                if hasattr(solveableclause, "blocks") and solveableclause.blocks(
                    model, clause
                ):
                    conflict = solveableclause
                    break

            def find_dependency(modstr: str):
                # Ignore top-level dependencies
                if not isinstance(modstr, Atom):
                    return None

                for solveableclause in solveableformula:
                    if isinstance(solveableclause, Formula.DepClause):
                        if atom_sat(Atom(modstr), solveableclause.dependency) and all(
                            var in model for var in solveableclause.requirements
                        ):
                            return solveableclause
                return None

            exceptionstring = f"{clause}\n"
            parent = find_dependency(clause.source)
            i = 1
            while parent is not None:
                exceptionstring += i * "  " + f"{parent}\n"
                parent = find_dependency(parent.source)
                i += 1

            if conflict:
                exceptionstring += "Contradicts:\n"
                exceptionstring += f"{conflict}\n"
                parent = find_dependency(conflict.source)
                i = 1
                while parent is not None:
                    exceptionstring += i * "  " + f"{parent}\n"
                    parent = find_dependency(parent.source)
                    i += 1

            raise DepError(f"Unable to satisfy dependencies:\n{exceptionstring}")

    raise Exception(
        "Internal error: Unable to satisfy dependencies, "
        "but there are no clauses in the formula!"
    )
