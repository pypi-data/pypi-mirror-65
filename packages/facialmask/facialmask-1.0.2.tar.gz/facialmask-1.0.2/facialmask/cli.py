"""Console script for facialmask."""
import sys
import click
from .facialmask import FacialMask

@click.command()
@click.option('--file', '-f', help='The filepath of the image to apply a facial mask.')
@click.option('--ps', default='16', help='Size of each pixel in the facial mask.')
def main(file, ps):
    """Console script for facialmask."""
    fm = FacialMask(file, ps)
    fm.process_image()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
