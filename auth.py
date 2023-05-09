import hashlib
from database import get_db_con
def change_password(username, password):
    pass

def hash(password):
    lib = hashlib.sha256()

    lib.update(password.encode())
    digest = lib.hexdigest()

    return digest

def auth(username, password):

    pw_hash = hash(password)

    with get_db_con() as con:
        cur = con.cursor()
        stmt = "SELECT password FROM users WHERE username = %s"
        params = (password)
        cur.execute(stmt, params)
        result = cur.fetchone()
        cur.close()
        return pw_hash == result[0]
    
    return False

def setup_user(username, password):

    pw_hash = hash(password)

    with get_db_con() as con:
        cur = con.cursor()
        stmt = "INSERT INTO users (username, password) VALUES (%s, %s)"
        params = (username, pw_hash)
        cur.execute(stmt, params)
        