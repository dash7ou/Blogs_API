from passlib.context import CryptContext


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():
    def bcrypt(password: str):
        return pwd_cxt.hash(password)
    
    def verify(user_password: str, request_password: str):
        return pwd_cxt.verify(request_password, user_password)