import numpy as np
import pandas as pd
from bio_test_artifacts._loader import Load

TSV_SUFFIX = ".tsv"


def counts_tsv_generate(num_obs=25, num_genes=5000, random_seed=42, integer=True, target_file=None, n=100, p=0.1,
                        transpose=False):
    """
    Generate a random TSV count or TPM matrix

    :param num_obs: Number of observations / samples. Defaults to 25
    :type num_obs: int, optional
    :param num_genes: Number of genes. Defaults to 5000
    :type num_genes: int, optional
    :param random_seed: Seeding for RNG. Defaults to 42
    :type random_seed: int, optional
    :param target_file: File target. Optional. Will create a temp file in $TMP if not set.
    :type target_file: str, optional
    :param integer: Generate an integer count matrix if True. Converts to float TPM if False. Defaults to True
    :type integer: bool, optional
    :param n: Negative binomial N parameter. Defaults to 100
    :type n: int, optional
    :param p: Negative binomial p parameter. Defaults to 0.1
    :type p: float, optional
    :param transpose: Transposes to Genes by Samples if True. Defaults to False
    :type transpose: bool, optional
    :return: An absolute pathname to a TSV file and a pandas dataframe containing counts
    :rtype: str, pd.DataFrame
    """

    random_generator = np.random.RandomState(random_seed)
    target_file = Load.make_test_file(suffix=TSV_SUFFIX) if target_file is None else target_file

    counts = pd.DataFrame(random_generator.negative_binomial(n, p, size=(num_obs, num_genes)),
                          columns=list(map(lambda x: "Gene" + str(x), range(num_genes))))
    if not integer:
        counts = np.divide(counts, counts.sum(axis=1).values.reshape(-1, 1)) * 1000000

    if transpose:
        counts = counts.transpose()

    counts.to_csv(target_file, sep="\t", index=False)

    return target_file, counts
