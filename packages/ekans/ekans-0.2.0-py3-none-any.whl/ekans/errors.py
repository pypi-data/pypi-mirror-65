"""``ekans.errors`` -- Exceptions used in the package

This module defines the complete set of errors that are expected to happen in
the execution. Each of them is of different nature and the details are to be
seen in the documentation of each error, respectively.

"""


class MismatchingPackagesException(Exception):
    """The dependencies compared references to different packages.

    A Dependency can be compared with other to check for version order, as long
    as they refer to the same package. If not, this exception is thrown.
    """

    def __init__(self, msg: str):
        super().__init__(msg)


class NoReproducibilityEnsuredException(Exception):
    """An environment was found to have not ensured reproducibility.

    This exception contains a message to be displayed when the required
    environment has failed the checks.

    Attributes:
        msg (str): the error message.
    """

    def __init__(self, env):
        self.msg = f"{env.name} is not fully reproducible"
        super().__init__(self.msg)


class DisjointChannelsException(Exception):
    """The channels defined in two environments do not match

    This exception contains the error details and message, and presents the
    information in an easy to understand string.

    Attributes:
        missing_dev (Set[str]): channels missing from dev.
        missing_prod (Set[str]): channels missing from prod.
        msg (str): error message.
    """

    def __init__(self, dev, prod):
        self.missing_prod = dev.channels - prod.channels
        self.missing_dev = prod.channels - dev.channels
        self.msg = self._generate_msg()
        super().__init__(self.msg)

    def _generate_msg(self) -> str:
        msg = "Not both channel sets are the same.\n"
        if self.missing_dev:
            msg += f"\tMissing from dev: {', '.join(self.missing_dev)}\n"
        if self.missing_prod:
            msg += f"\tMissing from prod: {', '.join(self.missing_prod)}\n"
        return msg


class DisjointDependenciesException(Exception):
    """There are dependencies defined in prod but not in dev.

    This exception contains the error details and message, and presents the
    information in an easy to understand string.

    Attributes:
        missing_dev (Set[Dependency]): dependencies missing from dev.
        msg (str): error message.
    """

    def __init__(self, dev, prod):
        self.missing_dev = prod.dependencies - dev.dependencies
        self.msg = self._generate_msg()
        super().__init__(self.msg)

    def _generate_msg(self) -> str:
        msg = f"{len(self.missing_dev)} dependencies are missed from dev.\n"
        msg += "\nComplete list:\n"
        for dep in self.missing_dev:
            msg += f"\t- {dep}\n"
        return msg
