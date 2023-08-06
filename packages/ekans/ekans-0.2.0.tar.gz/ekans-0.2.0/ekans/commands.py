import sys
import click

import ekans.checks as checks
import ekans.errors as errors

from ekans.entities import Environment


cli = click.Group()


@cli.command()
@click.option(
    "-f",
    "--filename",
    type=click.Path(),
    prompt="Path to environment",
    help="Environment file to check (in YAML format).",
)
def fixed(filename: str):
    """Check if an environment.yml defines a reproducible environment.

    An environment is reproducible if all its dependencies have fixed versions
    defined: that is not only a version definition but no wildcards used. This
    should result in Conda always fetching the same concrete packages and
    creating from scratch the same working environment.
    """
    with open(filename, "r") as stream:
        env = Environment.from_yaml(stream)

    try:
        checks.verify_fixed_state(env)
        print(f"{env.name} is fully reproducible.")
    except errors.NoReproducibilityEnsuredException:
        print(f"{env.name} is not fully reproducible.")
        sys.exit(1)


@cli.command()
@click.option(
    "-p",
    "--prod",
    type=click.Path(),
    default="./envs/prod.yml",
    help="Production environment file (in YAML format).",
)
@click.option(
    "-d",
    "--dev",
    type=click.Path(),
    default="./envs/dev.yml",
    help="Development environment file (in YAML format).",
)
def verify(dev: str, prod: str):
    """Check if two environments define proper dev and prod environments.

    Checks if two environments generate sound production and development
    environments.  The basic idea is that the production environment should
    define a subset of the development one (without the development
    dependencies) and the prod dependencies should have a fixed version in
    order to be reproducible.
    """
    with open(dev, "r") as stream:
        dev_env = Environment.from_yaml(stream)

    with open(prod, "r") as stream:
        prod_env = Environment.from_yaml(stream)

    try:
        checks.verify_dev_prod_setup(dev=dev_env, prod=prod_env)
    except (
        errors.NoReproducibilityEnsuredException,
        errors.DisjointChannelsException,
        errors.DisjointDependenciesException,
    ) as e:
        print(e.msg)
        sys.exit(1)

    checks.verify_dependencies(prod_env, prod_env)
