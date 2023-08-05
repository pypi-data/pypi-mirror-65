import os
from bio_test_artifacts._loader import Load
_data_path = os.path.join(os.path.dirname(__file__), "artifacts")

_YEAST_CHR01_FASTA_FILE_NAME = "yeast_chr01.fasta"
_YEAST_CHR01_PROTEIN_FASTA_FILE_NAME = "yeast_chr01_protein.fasta"


def fasta_yeast_chr01():
    """
    Make a FASTA file containing yeast chromosome 1 (chr1).

    :returns: An absolute path to the FASTA file and a list [(header, sequence)]
    :rtype: str, list(tuple(str, str))
    """
    from bio_test_artifacts.prebuilt._yeast_fasta import _YEAST_CHR01_SEQ, _YEAST_CHR01_HEADER

    copied_file = Load.copy_test_file(os.path.join(_data_path, _YEAST_CHR01_FASTA_FILE_NAME))
    return copied_file, [(_YEAST_CHR01_HEADER, _YEAST_CHR01_SEQ)]


def fasta_protein_yeast_chr01():
    """
    Make a FASTA file containing the first two protein sequences located on yeast chromosome 1 (chr1).

    :returns: A path to the FASTA file and a list [(header0, sequence0), (header1, sequence1)]
    :rtype: str, list(tuple(str, str))
    """

    from bio_test_artifacts.prebuilt._yeast_fasta import (_YEAST_CHR01_PROTEIN_1_HEADER, _YEAST_CHR01_PROTEIN_1_SEQ,
                                                          _YEAST_CHR01_PROTEIN_2_HEADER, _YEAST_CHR01_PROTEIN_2_SEQ)

    copied_file = Load.copy_test_file(os.path.join(_data_path, _YEAST_CHR01_PROTEIN_FASTA_FILE_NAME))
    return copied_file, [(_YEAST_CHR01_PROTEIN_1_HEADER, _YEAST_CHR01_PROTEIN_1_SEQ),
                         (_YEAST_CHR01_PROTEIN_2_HEADER, _YEAST_CHR01_PROTEIN_2_SEQ)]
