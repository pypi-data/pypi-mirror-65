import hashlib
from lhub_integ.common import file_manager_client


def get_hash_custom(lhub_file_id, hashlib_object):
    """
    Takes a file and generates a hash based on the provided hashing object. The hashing object can either be one of
    hashlib's builtin functions or a custom object defined with hashlib.new(). (Note that there are other functions
    below to make it easier to get a specific type of hash.)

    Args:
        lhub_file_id (str):
            Name of a file created using file_manager_client

        hashlib_object (_hashlib.HASH object):
            Either a custom hash object created by hashlib.new() or one of the built-in functions:
                hashlib.md5()
                hashlib.sha1()
                hashlib.sha224()
                hashlib.sha256()
                hashlib.sha384()
                hashlib.sha512()

    Returns:
        (str): File hash string

    """
    file_to_hash = file_manager_client.openFileForReading(lhub_file_id, 'rb')
    for chunk in iter(lambda: file_to_hash.fd.read(4096), b""):
        hashlib_object.update(chunk)
    file_to_hash.close()
    return hashlib_object.hexdigest()


def get_hash_md5(lhub_file_id):
    return get_hash_custom(lhub_file_id, hashlib.md5())


def get_hash_sha1(lhub_file_id):
    return get_hash_custom(lhub_file_id, hashlib.sha1())


def get_hash_sha256(lhub_file_id):
    return get_hash_custom(lhub_file_id, hashlib.sha256())


def get_file_size(lhub_file_id):
    f = file_manager_client.openFileForReading(lhub_file_id)
    s = f.size()
    f.close()
    return s


def get_mime_type(lhub_file_id):
    return file_manager_client.get_mime_type(lhub_file_id)


def get_file_encoding(lhub_file_id):
    f = file_manager_client.openFileForReading(lhub_file_id)
    encoding_info = f.encoding()
    return encoding_info


def get_file_details(lhub_file_id):
    # compute the md5 hash
    md5_hash = get_hash_md5(lhub_file_id)
    # compute the sha1 hash
    sha1_hash = get_hash_sha1(lhub_file_id)
    # compute the sha256 hash
    sha256_hash = get_hash_sha256(lhub_file_id)
    # get the size of the file
    size = get_file_size(lhub_file_id)
    # guess its mime-type
    mime = get_mime_type(lhub_file_id)
    # guess its encoding
    encoding_info = get_file_encoding(lhub_file_id)
    result = {
        "hash_md5": md5_hash,
        "hash_sha1": sha1_hash,
        "hash_sha256": sha256_hash,
        "size": size,
        "content_type": mime,
        "encoding_info": encoding_info,
    }
    return result


def compute_file_hash(lhub_file_id):
    """
    Legacy method used to generate only an MD5 hash. This should no longer be used in new integrations. For md5 hashes,
    use get_hash_md5

    ToDo Remove this method once it is no longer used by any integrations
    """
    file_to_hash = file_manager_client.openFileForReading(lhub_file_id)
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: file_to_hash.fd.read(4096), b""):
        hash_md5.update(chunk)
    file_to_hash.close()
    return hash_md5.hexdigest()
