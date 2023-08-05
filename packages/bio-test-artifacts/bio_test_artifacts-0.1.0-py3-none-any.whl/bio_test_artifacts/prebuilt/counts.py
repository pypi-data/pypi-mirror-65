import pandas as pd
import os

from bio_test_artifacts._loader import Load

_data_path = os.path.join(os.path.dirname(__file__), "artifacts")

_YEAST_COUNTS_TPM_FILE_NAME = "GSE135430_counts_TPM.tsv"
_YEAST_COUNTS_TPM_CHR01_FILE_NAME = "GSE135430_counts_chr01_TPM.tsv"
_YEAST_COUNTS_SS_TSV_FILE_NAME = "GSE125162_counts_chr01.tsv.gz"
_YEAST_COUNTS_SS_HDF5_FILE_NAME = "GSE125162_counts_chr01.hdf5.gz"
_YEAST_COUNTS_SS_H5AD_FILE_NAME = "GSE125162_counts_chr01.h5ad.gz"

_YEAST_COUNTS_SS_MTX_FILE_NAME = "GSE125162_counts_chr01.mtx.gz"
_YEAST_COUNTS_SS_MTX_GENES_FILE_NAME = "GSE125162_counts_chr01_genes.tsv.gz"
_YEAST_COUNTS_SS_MTX_OBS_FILE_NAME = "GSE125162_counts_chr01_features.tsv.gz"


def counts_yeast_tpm(gzip=False):
    """
    Make a count TSV file from GEO record GSE135430.
    This will have 12 non-header rows and 6685 gene columns. All values are floats.
    It is in Transcripts Per Million (TPM) and all rows should approximately sum to 1e6

    :param gzip: Provide a gzipped (.gz) file instead of a .tsv file. Defaults to False.
    :type gzip: bool
    :returns: An absolute path to the count TSV file and a pandas DataFrame (12 x 6685)
    :rtype: str, pd.DataFrame
    """
    file = os.path.join(_data_path, _YEAST_COUNTS_TPM_FILE_NAME)

    copied_file = Load.copy_test_file(file, gzip=gzip)

    return copied_file, pd.read_csv(file, sep="\t", index_col=None)


def counts_yeast_tpm_chr01(gzip=False):
    """
    Make a count TSV file from GEO record GSE135430.
    This will have 12 non-header rows and 121 gene columns. All values are floats.
    It is in Transcripts Per Million (TPM), but it is a subset of the entire genome and rows do not sum to 1e6.

    :param gzip: Provide a gzipped (.gz) file instead of a .tsv file. Defaults to False.
    :type gzip: bool
    :returns: An absolute path to the count TSV file and a pandas DataFrame (12 x 121)
    :rtype: str, pd.DataFrame
    """
    file = os.path.join(_data_path, _YEAST_COUNTS_TPM_CHR01_FILE_NAME)

    copied_file = Load.copy_test_file(file, gzip=gzip)

    return copied_file, pd.read_csv(file, sep="\t", index_col=None)


def counts_yeast_single_cell_chr01(gzip=False, filetype='tsv'):
    """
    Make a count TSV file from GEO record GSE125162.
    This will have 38225 non-header rows and 121 gene columns. All values are integers.
    It is in (UMI) counts.

    :param gzip: Provide a gzipped (.gz) file instead of a .tsv file. Defaults to False.
    :type gzip: bool
    :param filetype: Which type of count file to provide. Options are TSV, MTX, HDF5, and H5AD
    :type filetype: str
    :returns: An absolute path to the count file and a pandas DataFrame (38225 x 121)
        In the case of the MTX option, a tuple of .mtx, .genes.tsv, and .features.tsv will be returned
        instead of a single path.
    :rtype: str, pd.DataFrame
    """
    tsv_data = pd.read_csv(os.path.join(_data_path, _YEAST_COUNTS_SS_TSV_FILE_NAME), sep="\t", index_col=None)

    if filetype.lower() == "tsv":
        file = os.path.join(_data_path, _YEAST_COUNTS_SS_TSV_FILE_NAME)
    elif filetype.lower() == "hdf5":
        file = os.path.join(_data_path, _YEAST_COUNTS_SS_HDF5_FILE_NAME)
    elif filetype.lower() == "h5ad":
        file = os.path.join(_data_path, _YEAST_COUNTS_SS_H5AD_FILE_NAME)
    elif filetype.lower() == "mtx":
        mtx_file = Load.copy_test_file(os.path.join(_data_path, _YEAST_COUNTS_SS_MTX_FILE_NAME), unzip=not gzip)
        mtx_obs = Load.copy_test_file(os.path.join(_data_path, _YEAST_COUNTS_SS_MTX_OBS_FILE_NAME), unzip=not gzip)
        mtx_gene = Load.copy_test_file(os.path.join(_data_path, _YEAST_COUNTS_SS_MTX_GENES_FILE_NAME), unzip=not gzip)
        return (mtx_file, mtx_gene, mtx_obs), tsv_data
    else:
        raise ValueError("filetype must be tsv, mtx, hdf5, or h5ad")

    copied_file = Load.copy_test_file(file, unzip=not gzip)

    return copied_file, tsv_data
