import tempfile
import shutil
import os
import subprocess


class Load:

    _temp_path = None
    _temp_files = None

    @classmethod
    def copy_test_file(cls, file, gzip=False, unzip=False):
        cls._check_init()

        # Make sure the file is an absolute path
        file = os.path.abspath(os.path.expanduser(file))

        # Make a temp file and close the file descriptor
        extension = os.path.basename(file).split(os.extsep, 1)
        extension = extension[1] if len(extension) == 2 else ""
        fd, tmp_file_name = tempfile.mkstemp(suffix=extension, dir=cls._temp_path.name)
        os.close(fd)

        # Copy the test file
        shutil.copy(file, tmp_file_name)

        if gzip:
            subprocess.check_call(['gzip', tmp_file_name])
            tmp_file_name += ".gz"

        if unzip:
            subprocess.check_call(['gunzip', tmp_file_name])
            if tmp_file_name.endswith(".gz"):
                tmp_file_name = tmp_file_name[:-3]

        cls._temp_files.append((file, tmp_file_name))

        return tmp_file_name

    @classmethod
    def make_test_file(cls, prefix=None, suffix=None):
        cls._check_init()

        # Make a temp file and close the file descriptor
        fd, tmp_file_name = tempfile.mkstemp(prefix=prefix, suffix=suffix, dir=cls._temp_path.name)
        os.close(fd)

        cls._temp_files.append((None, tmp_file_name))

        return tmp_file_name

    @classmethod
    def _check_init(cls):
        if cls._temp_path is None:
            cls._temp_path = tempfile.TemporaryDirectory(prefix="bio_test_")

        if cls._temp_files is None:
            cls._temp_files = []