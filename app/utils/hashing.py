from passlib.context import CryptContext

pwd_context = CryptContext(schemes = ["bcrypt"],deprecated="auto")
def hash_password(password):
  hashed_passord = pwd_context.hash(password)
  return hashed_passord

def verify_password(plain_password , hashed_password):
	return pwd_context.verify(plain_password , hashed_password)