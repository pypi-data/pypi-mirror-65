import sys
import click

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
def verify(filename: str) -> bool:
    """Check if an environment.yml defines a reproducible environment.

    An environment is reproducible if all its dependencies have fixed versions
    defined: that is not only a version definition but no wildcards used. This
    should result in Conda always fetching the same concrete packages and
    creating from scratch the same working environment.

    Args:
        filename: path to the environment YAML file.

    Returns:
        Whether the YAML defines a completely reproducible package or not.

    """
    with open(filename, "r") as stream:
        env = Environment.from_yaml(stream)

    if env.is_reproducible:
        print(f"{env.name} is fully reproducible.")
        sys.exit(0)
    else:
        print(f"{env.name} is not fully reproducible.")
        sys.exit(-1)
