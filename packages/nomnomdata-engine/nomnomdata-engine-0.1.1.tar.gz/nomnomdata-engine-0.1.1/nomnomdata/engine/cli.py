import click

from .run import run
from .run_tests import run_mock, run_tests


@click.group(name="engine")
def cli():
    """NomNomData Engine CLI, used for the execution of engines"""


@cli.command()
def test():
    """Run unittests for the nomnomdata-engine module"""
    import pytest

    pytest.main(["--pyargs", "nomnomdata.engine"])


cli.add_command(run)
cli.add_command(run_tests)
cli.add_command(run_mock)
