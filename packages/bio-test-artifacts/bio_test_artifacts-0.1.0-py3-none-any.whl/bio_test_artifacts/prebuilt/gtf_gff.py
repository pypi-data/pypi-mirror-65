import os

from bio_test_artifacts._loader import Load

_data_path = os.path.join(os.path.dirname(__file__), "artifacts")

_YEAST_GTF_CHR01 = "yeast_chr01.gtf"
_YEAST_GFF_CHR01 = "yeast_chr01.gtf"


def gtf_yeast_chr01(gzip=False):
    """
    Make a GTF that covers yeast chromosome 1.

    :param gzip: Provide a gzipped GTF (.gtf.gz). Defaults to False.
    :type gzip: bool
    :returns: The absolute paths to the GTF file
    :rtype: str
    """
    file = os.path.join(_data_path, _YEAST_GTF_CHR01)

    copied_file = Load.copy_test_file(file, gzip=gzip)

    return copied_file


def gff_yeast_chr01(gzip=False):
    """
    Make a GFF that covers yeast chromosome 1.

    :param gzip: Provide a gzipped GTF (.gff.gz). Defaults to False.
    :type gzip: bool
    :returns: The absolute paths to the GTF file
    :rtype: str
    """
    file = os.path.join(_data_path, _YEAST_GTF_CHR01)

    copied_file = Load.copy_test_file(file, gzip=gzip)

    return copied_file
