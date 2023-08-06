"""``ekans.checks`` -- Checks to be done to the environments.

This module defines the checks to be done when verifying the integrity of a
development/production setup in Conda packages. Each check throws an Exception
(defined in `ekans.errors`) and can, therefore, be used anywhere in the code
following the usual error checking strategies.

"""
import ekans.errors as errors
from ekans.entities import Environment


def verify_fixed_state(env: Environment):
    """Ensure that the environment can be safely reproduced.

    An environment can be reproduced if all its dependencies have a fixed
    version. This function is silent if succesful, and raises an exception
    if the condition is not fulfilled.

    Args:
        env: environment to check for reproducibility.

    Raises:
        `ekans.errors.NoReproducibilityEnsuredException` if the check fails.

    """
    if not env.is_reproducible:
        raise errors.NoReproducibilityEnsuredException(env)


def verify_channels(dev: Environment, prod: Environment):
    """Verify the channel definition in both dev and prod environments.

    In order for a dev environment to properly mimic the prod one's behaviour,
    the channel definition on both must be the same. If not, different packages
    could be fetch with the same name from different channels, causing hard to
    debug errors. This function is silent if succesful, and raises an exception
    if the condition is not fulfilled.

    Args:
        dev: development environment to verify.
        prod: production environment as reference.

    Raises:
        `ekans.errors.DisjointChannelsException` if the check fails.

    """
    if dev.channels != prod.channels:
        raise errors.DisjointChannelsException(dev, prod)


def verify_dependencies(dev: Environment, prod: Environment):
    """Verify the dependency definition in both dev and prod environments.

    In order for a dev environment to properly mimic the prod one's behaviour,
    the dependency definition must be a strict superset of the production's
    one. If not, there are some missing packages in production. This function
    is silent if succesful, and raises an exception
    if the condition is not fulfilled.

    Args:
        dev: development environment to verify.
        prod: production environment as reference.

    Raises:
        `ekans.errors.DisjointDependenciesException` if the check fails.

    """
    if prod.dependencies - dev.dependencies:
        raise errors.DisjointDependenciesException(dev, prod)


def verify_dev_prod_setup(dev: Environment, prod: Environment):
    """Verify that the dev definiton is sound, taking prod as a reference.

    This function runs all checks needed to verify that the development
    environment generates a superset of the production one. To check it, three
    checks are required:
        - Verifying that production is completely reproducible.
        - Verifying that both environments have the same channels defined.
        - Verifying that prod's dependencies are a subset of dev's.

    If these three checks pass, we can assume that the environment is setup is
    correct. If not, an exception is raised defining the issue.

    Args:
        dev: development environment to verify.
        prod: production environment as reference.

    Raises:
        `ekans.errors.NoReproducibilityEnsuredException`, if the
            reproducibility check fails.
        `ekans.errors.DisjointChannelsException`, if the channel check fails.
        `ekans.errors.DisjointDependenciesException`, if the dependency check
            fails.

    """
    verify_fixed_state(prod)
    verify_channels(dev, prod)
    verify_dependencies(dev, prod)
