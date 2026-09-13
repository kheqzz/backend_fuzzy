import datetime
from uuid import UUID
import jwt  
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from app.core.config import settings
from app.core import exceptions as ex

pwd_context = PasswordHash([BcryptHasher()])

def get_password_hash(password: str) -> str:
    """Hash a plaintext password."""
    return pwd_context.hash(password)


def get_password_verify(password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its hash."""
    return pwd_context.verify(password, hashed_password)


def create_access_token(
    *,
    secrets: dict,
    expiration_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
) -> str:
    """
    Create a JWT token.

    Args:
        secrets: Dictionary containing at least ``secret`` and ``algorithm`` keys.
        expiration_minutes: Token expiration in minutes (default reads from settings).

    Returns:
        A signed JWT string.
    """
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    expire = now + datetime.timedelta(minutes=expiration_minutes)
    payload = {
        "exp": expire,
    }
    payload.update(secrets)
   

    return jwt.encode(payload,settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> UUID:
    """
    Decode a JWT token and return its payload.

    Args:
        token: JWT string.
        secrets: Same dictionary used for signing.

    Returns:
        Payload dictionary.

    Raises:
        jwt.exceptions.InvalidTokenError: If token is invalid or expired.
    """
    exception = ex.UnauthorizedError(message="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id_raw = payload.get('sub')
    
            if not user_id_raw:
                raise exception
        
            try : user_id = UUID(str(user_id_raw))
            except ValueError:
                raise exception
    
            if user_id is None:
                raise exception
            return user_id
            
    except jwt.PyJWTError:
            raise exception


class AuthError(Exception):
    """Base class for authentication-related errors."""

    def __init__(self, message: str, status_code: int = 401):
        super().__init__(message)
        self.status_code = status_code