import fastapi.security as security
from pwdlib import PasswordHash

SECRET_KEY = "46810de1ffee764917b80678b169d1b829ceda1b2ddd0a8e01b88cb01902dbf9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hasher = PasswordHash.recommended()
oauth2_scheme = security.OAuth2PasswordBearer(tokenUrl="token")