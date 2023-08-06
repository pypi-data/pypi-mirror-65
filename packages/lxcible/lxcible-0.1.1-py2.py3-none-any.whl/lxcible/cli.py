"""Console script for lxcible."""
import sys
import click
from lxcible import lxcible


@click.command()
@click.version_option()
@click.option('--list', 'option', flag_value='list', required=True,
              help="""
                   Output dyamic Ansible inventory based on running
                   linuxcontainers
                   """,
              )
def main(option=None):
    """
    main command
    """
    if option == 'list':
        inventory = lxcible.LxcInventory()
        inventory.dump()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
