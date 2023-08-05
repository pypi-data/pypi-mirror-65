import os

from bio_test_artifacts._loader import Load

_data_path = os.path.join(os.path.dirname(__file__), "artifacts")

_SRR1569870_SAM = "SRR1569870_1.sam"
_SRR1569870_BAM_UNSORT = "SRR1569870_1.bam"
_SRR1569870_BAM_SORT = "SRR1569870_1.sorted.bam"


def sam_paired_end(gzip=False):
    """
    Make a paired-end alignment SAM file from SRR1569870 FASTQ data.
    Alignment performed with BWA MEM.
    Contains two header lines and 1000 alignment lines (500 paired-end alignments),

    :param gzip: Provide a gzipped SAM (.sam.gz). Defaults to False.
    :type gzip: bool
    :returns: The absolute paths to the SAM file
    :rtype: str
    """
    file = os.path.join(_data_path, _SRR1569870_SAM)

    copied_file = Load.copy_test_file(file, gzip=gzip)

    return copied_file


def bam_paired_end_unsorted():
    """
    Make a paired-end alignment SAM file from SRR1569870 FASTQ data.
    Alignment performed with BWA MEM.
    Contains 1000 alignments (500 paired-end alignments).
    Has not been sorted.

    :returns: The absolute paths to the SAM file
    :rtype: str
    """

    file = os.path.join(_data_path, _SRR1569870_BAM_UNSORT)

    copied_file = Load.copy_test_file(file)

    return copied_file


def bam_paired_end_sorted():
    """
    Make a paired-end alignment SAM file from SRR1569870 FASTQ data.
    Alignment performed with BWA MEM.
    Contains 1000 alignments (500 paired-end alignments).
    Has been sorted with samtools sort.

    :returns: The absolute paths to the SAM file
    :rtype: str
    """

    file = os.path.join(_data_path, _SRR1569870_BAM_SORT)

    copied_file = Load.copy_test_file(file)

    return copied_file
