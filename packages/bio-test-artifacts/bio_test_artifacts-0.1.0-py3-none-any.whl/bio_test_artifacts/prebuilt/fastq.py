import os

from bio_test_artifacts._loader import Load

_data_path = os.path.join(os.path.dirname(__file__), "artifacts")

_SRR1569870_FASTQ_1 = "SRR1569870_1.fastq.gz"
_SRR1569870_FASTQ_2 = "SRR1569870_2.fastq.gz"


def fastq_single_end(gzip=True):
    """
    Make a single-end FASTQ file from NCBI SRR1569870
    This will have 10580 sequences, each of which is 101bp.
    The PHRED scores are Illumina (PHRED +33)

    :param gzip: Provide a gzipped FASTQ (.fastq.gz). Defaults to True.
    :type gzip: bool
    :returns: The absolute paths to two FASTQ files
    :rtype: str, str
    """
    file = os.path.join(_data_path, _SRR1569870_FASTQ_1)

    copied_file = Load.copy_test_file(file, unzip=not gzip)

    return copied_file


def fastq_paired_end(gzip=True):
    """
    Make two paired-end FASTQ files from NCBI SRR1569870
    Both will have 10580 sequences, each of which is 101bp.
    The PHRED scores are Illumina (PHRED + 33)

    :param gzip: Provide a gzipped FASTQ (.fastq.gz). Defaults to True.
    :type gzip: bool
    :returns: The absolute paths to two FASTQ files
    :rtype: str, str
    """
    file1 = os.path.join(_data_path, _SRR1569870_FASTQ_1)
    file2 = os.path.join(_data_path, _SRR1569870_FASTQ_2)

    copied_file_1 = Load.copy_test_file(file1, gzip=gzip)
    copied_file_2 = Load.copy_test_file(file2, gzip=gzip)

    return copied_file_1, copied_file_2
