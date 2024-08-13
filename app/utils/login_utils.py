from bcrypt import hashpw, gensalt, checkpw


def hash_password(password: str) -> str:
    """A helper function that verifies user password against the hash"""

    salt = gensalt()
    pwd = password.encode()

    # Hash the password
    hashed_pwd = hashpw(pwd, salt)
    return hashed_pwd.decode()


def verify_password(password: str, hashed_pwd: str) -> bool:
    """A helper function that verifies user password against the hash"""

    if checkpw(password.encode(), hashed_pwd.encode()):
        return True

    return False
