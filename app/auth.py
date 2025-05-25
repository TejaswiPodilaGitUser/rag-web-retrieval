from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import os

# Load environment variables from .env
load_dotenv()

# Secret key and algorithm configuration for JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time in minutes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Function to create JWT token with expiration
def create_token(username: str):
    """
    Create a JWT token with an expiration time for the given username.
    """
    # Set expiration time for the token using timezone-aware datetime
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": username, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Function to extract current user from the token
def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Extract and return the current user based on the provided token.
    """
    try:
        # Decode the token and extract user information
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token has no username")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        # It's good to avoid catching generic Exception unless necessary
        raise HTTPException(status_code=401, detail=f"Error extracting user: {str(e)}")
