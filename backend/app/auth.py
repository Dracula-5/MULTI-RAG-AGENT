from passlib.context import CryptContext
from jose import jwt
from .config import SECRET_KEY

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pw(pw): return pwd.hash(pw)
def verify(pw, h): return pwd.verify(pw, h)

def create_token(data):
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")
def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
