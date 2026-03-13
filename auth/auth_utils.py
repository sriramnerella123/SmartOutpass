from passlib.context import CryptContext
from jose import jwt
from datetime import timedelta,datetime


SECRET_KEY = "mysupersecret"
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"])

async def hash_password(password:str):
    return pwd_context.hash(password)

async def verify_password(normal,hash):
    return pwd_context.verify(normal,hash)

def create_token(data:dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow()+timedelta(minutes=60)
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

