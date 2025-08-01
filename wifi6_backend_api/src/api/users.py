from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel, Field
from typing import Optional
from datetime import timedelta
from jose import JWTError, jwt

from src.api.utils import get_password_hash, verify_password, create_access_token

# Dummy users database substitute
fake_users_db = {
    "admin@example.com": {
        "username": "admin@example.com",
        "full_name": "Admin User",
        "hashed_password": get_password_hash("adminpass"),
        "disabled": False,
    },
}

SECRET_KEY = "REPLACE_ME_FOR_PRODUCTION"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Pydantic models
class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Type of the token")

class User(BaseModel):
    username: str = Field(..., description="User email/username")
    full_name: Optional[str] = Field(None, description="Full name")
    disabled: Optional[bool] = Field(False, description="Is the user disabled")

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    username: str = Field(..., description="User email/username")
    password: str = Field(..., description="Password")
    full_name: Optional[str] = Field(None, description="Full name")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# PUBLIC_INTERFACE
def get_user(db, username: str):
    """Get the user dict from db by username."""
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

# PUBLIC_INTERFACE
def authenticate_user(fake_db, username: str, password: str):
    """Validate credentials against the fake_db/dummy db."""
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# PUBLIC_INTERFACE
def get_current_user(token: str = Depends(oauth2_scheme)):
    """Obtain user from decoded JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username)
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=User, summary="Register a new user")
# PUBLIC_INTERFACE
def register(user: UserCreate):
    """Register a new user by username and password."""
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    fake_users_db[user.username] = {
        "username": user.username,
        "full_name": user.full_name,
        "hashed_password": hashed_password,
        "disabled": False,
    }
    return User(username=user.username, full_name=user.full_name, disabled=False)

@router.post("/login", response_model=Token, summary="Authenticate user and get access token")
# PUBLIC_INTERFACE
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate the user and generate a JWT access token.
    """
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username}, secret_key=SECRET_KEY, algorithm=ALGORITHM, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User, summary="Get current logged-in user's info")
# PUBLIC_INTERFACE
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Return the current authenticated user's info.
    """
    return current_user
