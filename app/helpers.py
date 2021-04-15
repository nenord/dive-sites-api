from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def parse_url(url):
    s1 = url.split('/')
    s11 = s1[2].split('@')[0]
    s12 = s1[2].split('@')[1]
    # return a list with username, password and url string
    return [s11.split(':')[0], s11.split(':')[1], 'http://' + s12]

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
