
import click

from ogr2wkt.util import convert_to_wkt


@click.command()
@click.argument('input_file')
@click.argument('output_file')
def ogr2wkt(input_file, output_file):
    """
    Write the contents of INPUT_FILE to OUTPUT_FILE as
    pipe-delimited text.
    """
    convert_to_wkt(input_file, output_file)
