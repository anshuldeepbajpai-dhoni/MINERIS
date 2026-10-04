from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.dependencies import get_db
from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)

        print("JWT PAYLOAD:", payload)

        user_id = payload.get("sub")

        if user_id is None:
            print("JWT ERROR: sub missing")
            raise credentials_exception

        user_id = int(user_id)

    except JWTError as exc:
        print("JWT ERROR:", repr(exc))
        raise credentials_exception

    except ValueError as exc:
        print("JWT VALUE ERROR:", repr(exc))
        raise credentials_exception

    user = db.get(User, user_id)

    if user is None or not user.is_active:
        raise credentials_exception

    return user