import textwrap
import numpy as np
from bio_test_artifacts._loader import Load

FASTA_SUFFIX = ".fasta"
FASTA_HEADER = "biotestartifact{n}"

DEFAULT_NUCLEOTIDE_ALPHABET = "ATGC"
DEFAULT_PROTEIN_ALPHABET = "ACDEFGHIKLMNPQRSTVWY"


def fasta_generate(num_records=20, record_length=100, random_seed=42, target_file=None,
                   alphabet=DEFAULT_NUCLEOTIDE_ALPHABET, probabilities=None):
    """
    Generate a random FASTA file

    :param num_records: Number of separate records to include in the file. Defaults to 20 records
    :type num_records: int, optional
    :param record_length: Length in bases of each individual record in the file, Defaults to 100 bases per record
    :type record_length: int, optional
    :param random_seed: Seeding for RNG. Defaults to 42
    :type random_seed: int, optional
    :param target_file: File target. Optional. Will create a temp file in $TMP if not set.
    :type target_file: str, optional
    :param alphabet: A string containing the alphabet for FASTA record, Defaults to ATGC
    :type alphabet: str, optional
    :param probabilities: An iterable with probabilities for each character in the alphabet string. Defaults to balanced
    :type probabilities: tuple(float), optional
    :return: An absolute pathname to a TSV file and a list of (header, seq) tuples
    :rtype: str, list(tuple())
    """

    probabilities = [1. / len(alphabet)] * len(alphabet) if probabilities is None else probabilities

    if len(alphabet) != len(probabilities):
        msg = "Alphabet ({a}) and probabilities ({p}) are of different length".format(a=len(alphabet),
                                                                                      p=len(probabilities))
        raise ValueError(msg)

    target_file = Load.make_test_file(suffix=FASTA_SUFFIX) if target_file is None else target_file

    random_generator = np.random.RandomState(random_seed)

    records = []
    with open(target_file, mode='w') as target_fh:
        for i in range(num_records):
            header = FASTA_HEADER.format(i)
            seq = "". join(random_generator.choice(list(alphabet), size=record_length, p=probabilities))

            print(">" + header, file=target_fh)
            print(textwrap.wrap(seq, width=120), file=target_fh)

            records.append((header, seq))

    return target_file, records


