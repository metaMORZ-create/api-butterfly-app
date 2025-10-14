from passlib.context import CryptContext

# zuerst bcrypt_sha256 für neue Hashes,
# bcrypt als Fallback, damit alte Hashes weiter verifizierbar bleiben
pwd_context = CryptContext(
    schemes=["bcrypt_sha256", "bcrypt"],
    deprecated="auto",
)

def hash_password(password: str) -> str:
    # erzeugt bcrypt_sha256-Hash
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # verifiziert automatisch gegen bcrypt_sha256 ODER bcrypt
    return pwd_context.verify(plain_password, hashed_password)
