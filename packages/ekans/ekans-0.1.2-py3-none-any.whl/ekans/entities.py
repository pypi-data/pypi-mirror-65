"""``ekans.entities`` -- Common classes to be used in the package.

This module defines the basic classes of Python objects to be used in the
package. These classes are simple metaphores of the objects to find in the
problem like dependencies of environments. Each of this declarations
encapsulates all the important notions to handle them: equality, ordering,
representation, etc... To ensure that the rest of the code does not have to
deal with this matters.

Todo:
    * Review if this module should be split in several smaller modules.

"""
import yaml
import re

from typing import Set, List, Optional, IO
from functools import total_ordering
from packaging.version import LegacyVersion

from ekans.errors import MismatchingPackagesException


@total_ordering
class Dependency:
    """A single dependency, that can optionally have versioning information.

    A dependency is formed by the name of a package and its versioning
    information. Dependencies can are equal if both its package and version
    (or lack of it) are the same. They are hashable following this criteria,
    so they can be used in sets and dictionary keys. If they represent the
    same package, they can be sorted as well: versions can be sorted from in
    ascending order from older to newer.

    Attributes:
        package (str): the name of the package it represents.
        version (:obj:`LegacyVersion`, optional): package version.

    """

    def __init__(self, package: str, version: Optional[str] = None):
        self.package = package
        self.version = LegacyVersion(version) if version else None

    @classmethod
    def from_declaration(cls: type, text: str) -> "Dependency":
        """Parse a Conda environment declaration into a Dependency instance.

        This method parses the typical Conda declaration of a package
        (accounting for possible whitespaces and miscellaneous characters) into
        a Dependency instance. If no versioning is found (not matching the
        regular expression), then the whole string is assumed to be the name of
        the package.
        """
        # This does not take into account comments because PyYAML ignores them.
        match = re.match(r"(?P<package>[\w|-]+?)\s*=\s*(?P<version>\S*)", text)

        if match:
            return cls(match.group("package"), match.group("version"))
        else:
            return cls(text)

    @property
    def is_versioned(self) -> bool:
        """Whether the Dependency has a version constraint or not."""
        return self.version is not None

    @property
    def is_fixed_versioned(self) -> bool:
        """Whether the Dependency has a fixed version or not."""
        if self.is_versioned:
            return "*" not in str(self.version)
        return False

    def __hash__(self) -> int:
        """Return the hash associated to this Depdendency.

        A Dependency is uniquely identified by its package name and its
        version number. Two dependencies referencing the same package and both
        lacking version information are indeed considered the same.
        """
        unique_id = self.package + str(self.version)
        return hash(unique_id)

    def __eq__(self, other):
        """Return if two Dependencies reference the same package and version.

        Two dependencies are equal if and only if they reference the same
        package and the same specific version. For that reason, two
        dependencies are the same only if they do not use wildcards in their
        version definition.

        """
        same_package = self.package == other.package
        same_version = (
            (self.version == other.version)
            and self.is_fixed_versioned
            and other.is_fixed_versioned
        )
        return same_package and same_version

    def __lt__(self, other):
        """Return if a Dependency is less than (earlier) than other.

        Two Dependencies can only be compared if they reference the same
        package. If that is not the case, the function will raise an exception
        indicating that it is not possible.

        Raises:
            MismatchingPackagesException: if the package name is different.

        """
        if self.package != other.package:
            raise MismatchingPackagesException(
                "cannot compare {self.package} and {other.package}'s versions."
            )

        return self.version < other.version

    def __repr__(self):
        return f"Dependency(package='{self.package}', version={self.version})"

    def __str__(self):
        if self.is_versioned:
            return f"{self.package}={self.version}"
        else:
            return self.package


class Environment:
    """A full representation of a Conda environment.

    An instance of this object allow the code to access the list of channels,
    dependencies, etc. This object also contains several useful properties to
    evaluate the current state of the environment. This class contains all some
    methods to parse a YAML file representing an environment as well.

    Attributes:
        name (str): the name of the environment.
        channels (Set[str]): list of all channels to fetch the packages from.
        dependencies (Set[Dependency]): list of all dependencies.

    """

    def __init__(self, name: str, channels: Set[str], dependencies: Set[Dependency]):
        self.name = name
        self.channels = channels
        self.dependencies = dependencies

    @classmethod
    def from_yaml(_, stream: IO) -> "Environment":
        """Read a YAML input stream into an Environment object.

        This parses the input of a YAML specifying the environment and its
        dependencies. It is expected to be written following the Conda tool
        guidelines as defined in the relevant `Conda Manual`_ section
        "Managing environments".

        Args:
            stream: a file-like object (as returned by ``open()``), in YAML
                format.

        Returns:
            The parsed Environment object.

        .. _Conda Manual:
            https://docs.conda.io/projects/conda/en/latest/user-guide

        """
        # TODO: add validation against schema
        data = yaml.safe_load(stream)

        name = data["name"]
        channels = set(data["channels"])
        dependencies = {Dependency.from_declaration(l) for l in data["dependencies"]}

        return Environment(name, channels, dependencies)

    @property
    def is_reproducible(self) -> bool:
        """An environment is reproducible if all its dependencies are versioned.

        This implies all its dependencies include a hard version constraint,
        that is, that no wildcards ("*") are used in any of the version
        numbers.

        Returns:
            If the environment can be reproduced or not.

        """
        return all(dep.is_fixed_versioned for dep in self.dependencies)

    def __eq__(self, other):
        """Two Environments are equal if they result in the same generation.

        Therefore, if the channels are the same, and the dependencies are the
        same, we can consider that two environments are equivalent (nevermind
        the name of each environment).

        Returns:
            If the environments are equivalent or not.

        """
        same_channels = self.channels == other.channels
        same_dependencies = self.dependencies == other.dependencies
        return same_channels and same_dependencies

    def __repr__(self):
        return f"Environment(name='{self.name}')"
