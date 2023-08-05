"""Console script for secretkey."""
import sys
import click

from .secretkey import generate_random_string


@click.command()
@click.argument("length")
def main(length):
    """Console script for secretkey."""
    print(generate_random_string(64))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
