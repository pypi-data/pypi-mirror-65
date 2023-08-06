import os
import errno
import uuid
import base64
import gzip


class File:
    def __init__(self, dir, name, mode, auto_unzip=True):
        """
        Open, read, and provide various attributes of a file. Unless auto_unzip is disabled, will automatically unzip
        before reading if the file is found to be compressed in a supported file type.

        :param dir: Path to the file
        :param name: File name
        :param mode: Edit mode for the file (e.g. 'r' to read, 'w' to write, etc.)
        :param auto_unzip: Optional: set to False to disable automatic decompression
        """
        self.auto_unzip = auto_unzip
        self.__path = os.path.join(dir, name)
        self.name = name
        if "r" in mode and self.auto_unzip and get_mime_type(self.name) == 'application/gzip':
            self.fd = gzip.open(self.__path, mode)
        else:
            self.fd = open(self.__path, mode)

    def close(self):
        self.fd.close()

    def path(self):
        return self.__path

    def size(self):
        return os.path.getsize(self.__path)

    def base64_content(self):
        return base64.b64encode(self.fd.read())

    def mime_type(self):
        import magic
        return magic.from_file(self.__path, mime=True)

    def encoding(self):
        import chardet
        with open(self.__path, 'rb') as f:
            encoding = chardet.detect(f.read())
        return encoding

    def remove(self):
        os.remove(self.__path)


def get_mime_type(lhub_file_id):
    f = openFileForReading(lhub_file_id)
    t = f.mime_type()
    f.close()
    return t


def create_directory(path):
    try:
        os.makedirs(path)
    except OSError as ex:
        if ex.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def ensure_directory_exists(base_dir):
    if not os.path.isdir(base_dir):
        create_directory(base_dir)


def get_base_integration_directory():
    base_dir = os.getenv("INTEGRATIONS_FILES_PATH", "/tmp")
    ensure_directory_exists(base_dir)
    return base_dir


BASE_INTEGRATION_DIRECTORY = get_base_integration_directory()


def openNewFileForWriting(extension=None, mode="w"):
    name = uuid.uuid4().hex
    if extension:
        name += "." + extension
    return File(BASE_INTEGRATION_DIRECTORY, name, mode)


def openFileForReading(name, mode="r", auto_unzip=False):
    """
    Reads a file based on the provided name and returns a file object. Assumes that the read mode is "rU" ("readUniversal") by
    default, but the mode can be overridden if desired (e.g. "rb" to read as a binary file").
    Using mode 'rU' to open a file for reading in universal newline mode

    :param str name: lhub file ID
    :param str mode: Optional: mode to use for opening the file if other than "r" ("read")
    :param bool auto_unzip: Optional: if a file is found to be a supported zip type, unzip it before reading contents
    :return: Returns a file object
    """
    return File(BASE_INTEGRATION_DIRECTORY, name, mode, auto_unzip)
