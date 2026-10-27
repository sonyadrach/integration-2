import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

password_hash = PasswordHash((BcryptHasher(),))

ALGORITHM = "HS256"

def read_secret(name: str) -> str:
    """Read secret value from /run/secrets/ ensuring fail-fast on missing file."""
    path = Path(f"/run/secrets/{name}")
    if not path.is_file():
        raise RuntimeError(f"Required secret '{name}' is missing at {path}")
    return path.read_text(encoding="utf-8").strip()

def get_jwt_secret() -> str:
    """Obtain token signing key exclusively from the mounted Docker secret."""
    return read_secret("jwt_secret_key")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the stored bcrypt hash."""
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate a bcrypt hash for the provided password."""
    return password_hash.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Generate a signed JWT access token with sub, iat, and exp claims."""
    to_encode = data.copy()
    now = datetime.now(timezone.utc)

    if expires_delta:
        expire = now + expires_delta
    else:
        minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        expire = now + timedelta(minutes=minutes)

    to_encode.update({"iat": now, "exp": expire})
    encoded_jwt = jwt.encode(to_encode, get_jwt_secret(), algorithm=ALGORITHM)
    return encoded_jwt