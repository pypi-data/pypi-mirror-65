import click

from readtagger.mateoperations import AnnotateMateInformation
from readtagger import VERSION


@click.command()
@click.option('-t',
              '--target',
              help='Annotate reads in this file with their mate sequence', required=True, type=click.Path(exists=True))
@click.option('-s',
              '--source',
              help='Use this file to find the mate sequence (can be same file as file_to_annotate)', required=True, type=click.Path(exists=True))
@click.option('-o',
              '--output_path',
              help='Write resulting BAM file to this path', required=True, type=click.Path(exists=False))
@click.option('-t',
              '--mate_sequence_tag', help='Use this tag to store the mate sequence', default='MS')
@click.version_option(version=VERSION)
def annotate_mate(**kwds):
    """Annotate reads with Mate Sequence in tag field."""
    AnnotateMateInformation(**kwds)
