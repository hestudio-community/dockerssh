import base64
import secrets
import passlib.hash


def generatepasswdhash(passwd: str) -> str:
    passwd_base64 = base64.b64encode(
        str(passlib.hash.sha512_crypt.hash(passwd)).encode("utf-8")
    )
    return passwd_base64.decode("utf-8")


def generatepasswd() -> str:
    passwd = secrets.token_hex(8)
    return passwd
