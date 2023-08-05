import os
import sys
from unittest import TestSuite, TestLoader, TextTestRunner
import click

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

LOADER = TestLoader()

# test suites
UNIT_TESTS = LOADER.discover("unit", top_level_dir=THIS_DIR)
INTEGRATION_TESTS = LOADER.discover("integration", top_level_dir=THIS_DIR)
VALIDATION_TESTS = LOADER.discover("validation", top_level_dir=THIS_DIR)

ALL_TESTS = TestSuite((UNIT_TESTS, INTEGRATION_TESTS, VALIDATION_TESTS))

# map command specified to each test suite
TESTS = {
    "unit": UNIT_TESTS,
    "integration": INTEGRATION_TESTS,
    "validation": VALIDATION_TESTS,
    "all": ALL_TESTS,
}


@click.group()
def tests():
    """cavcalc testing facility."""
    pass


@tests.command()
@click.argument("suite_names", nargs=-1, required=True)
@click.option(
    "-v",
    "--verbose",
    count=True,
    default=0,
    help='Enable verbose output. Supply extra flag for greater verbosity, i.e. "-vv".',
)
def run(suite_names, verbose):
    """Run test suites."""
    if verbose > 2:
        verbose = 2

    try:
        test_suites = [TESTS[suite_name] for suite_name in suite_names]
    except KeyError as e:
        click.echo(
            'Suite name %s is invalid (use "suites" to list available suites).' % e,
            err=True,
        )
        sys.exit()

    suite = TestSuite(test_suites)

    click.echo("Running %i tests" % suite.countTestCases())
    run_and_exit(suite, verbosity=verbose)


@tests.command()
def suites():
    """List available test suites."""
    click.echo(", ".join(TESTS))


def run_and_exit(suite, verbosity=1):
    """Run tests and exit with a status code representing the test result."""
    runner = TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())


if __name__ == "__main__":
    tests()
