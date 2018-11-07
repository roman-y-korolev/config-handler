import hashlib


def make_hash(password):
    """
    Make hash of user pass to store it in the database
    :param password: pass
    :type password: str
    :return: hash
    :rtype: str
    """
    return str(hashlib.sha512(password.encode('utf-8')).hexdigest())
