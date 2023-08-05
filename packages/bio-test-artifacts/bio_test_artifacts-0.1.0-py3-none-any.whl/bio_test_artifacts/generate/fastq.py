import numpy as np
import gzip
from bio_test_artifacts._loader import Load

DEFAULT_NUCLEOTIDE_ALPHABET = "ATGC"
FASTQ_SUFFIX = '.fastq'
FASTQ_HEADER = "GENERATE.{i} D4LHBFN1:249:D292YACXX:8:1101:{r1}:{r2} length={l}"


def _illumina_qual_to_num(qstr):
    return [ord(ch) - 33 for ch in qstr]


def _illumina_num_to_qual(qlist):
    return "".join([chr(va) for va in qlist])


def fastq_generate(num_sequences=100, seq_length=75, gzip_output=True,  random_seed=42, target_file=None,
                   alphabet=DEFAULT_NUCLEOTIDE_ALPHABET, probabilities=None):
    """
    Generate a random FASTQ file. PHRED scores will be illumina (+33).

    :param num_sequences: Number of separate sequence records to include in the file. Defaults to 100 records
    :type num_sequences: int, optional
    :param seq_length: Length in bases of each individual record in the file, Defaults to 75 bases per record
    :type seq_length: int, optional
    :param gzip_output: Should the output be a gzipped FASTQ. Defaults to True
    :type gzip_output: bool, optional
    :param random_seed: Seeding for RNG. Defaults to 42
    :type random_seed: int, optional
    :param target_file: File target. Optional. Will create a temp file in $TMP if not set.
    :type target_file: str, optional
    :param alphabet: A string containing the alphabet for FASTQ record, Defaults to ATGC
    :type alphabet: str, optional
    :param probabilities: An iterable with probabilities for each character in the alphabet string. Defaults to balanced
    :type probabilities: tuple(float), optional
    :return: An absolute pathname to a TSV file and a list of (header, seq, quality) tuples.
        Quality is a list of integer PHRED scores, not a character string
    :rtype: str, list(tuple())
    """

    probabilities = [1. / len(alphabet)] * len(alphabet) if probabilities is None else probabilities

    if len(alphabet) != len(probabilities):
        msg = "Alphabet ({a}) and probabilities ({p}) are of different length".format(a=len(alphabet),
                                                                                      p=len(probabilities))
        raise ValueError(msg)

    suffix = FASTQ_SUFFIX if not gzip_output else FASTQ_SUFFIX + ".gz"
    target_file = Load.make_test_file(suffix=suffix) if target_file is None else target_file

    opener = gzip.open if gzip_output else open
    random_generator = np.random.RandomState(random_seed)

    records = []
    with opener(target_file, mode="w") as fastq_fh:
        for i in range(num_sequences):

            # Generate data for this record
            loc = random_generator.randint(1, 99999, size=2)
            header = FASTQ_HEADER.format(i=i, r1=loc[0], r2=loc[1], l=seq_length)
            seq = "". join(random_generator.choice(list(alphabet), size=seq_length, p=probabilities))
            qual = [np.maximum(random_generator.normal(33, 4, size=seq_length).astype(int), 33)]

            # Print the data to the output file
            print("@" + header, file=fastq_fh)
            print(seq, file=fastq_fh)
            print("+" + header, file=fastq_fh)
            print(_illumina_num_to_qual(qual), file=fastq_fh)

            records.append((header, seq, qual))

    return target_file, records
