"""
Hash de contraseñas (RNF-01: nunca en texto plano).

TEMPORAL: usa PBKDF2 de la librería estándar para no añadir dependencias.
En la práctica de autenticación se sustituirá por bcrypt, como pide el documento.
"""

import hashlib
import hmac
import os

_ITERATIONS = 600_000


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, _ITERATIONS)
    return f"pbkdf2_sha256${_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password: str, hashed: str) -> bool:
    _, iterations, salt_hex, digest_hex = hashed.split("$")
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), int(iterations))
    return hmac.compare_digest(digest.hex(), digest_hex)
