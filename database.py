from config import *
import psycopg2

def get_db_con():

    conf = get_pg_conf()

    con = psycopg2.connect(
        host=conf[0],
        port=conf[1],
        database="testdb",
        user=conf[2],
        password=conf[3]
    )

    return con

def setup_database():

    queries = None

    with open('setup.sql', 'r') as file:
        queries = file.read()

    sql_querys = queries.split(';')
    
    with get_db_con() as con:
        cur = con.cursor()
        for command in sql_querys:
            try:
                cur.execute(command)
                con.commit()
            except:
                con.rollback()

def check_pg_db_con(url, port, username, password):

    try:
        with psycopg2.connect(
        host=url,
        port=port,
        database="testdb",
        user=username,
        password=password
    ) as con:
            return True
    except Exception as e:
        print(str(e))
        return False

def get_meta(key):

    try:
        with get_db_con() as con:
            stmt = "SELECT value FROM meta WHERE key = %s"
            cur = con.cursor()
            params = (key,)
            result = cur.execute(stmt, params)

            return result[0]
    except Exception as e:
        return None

def check_cache_db_con(url, port, username, password):
    return True

def is_configured():

    con_details = get_pg_conf()

    if not check_pg_db_con(con_details[0], con_details[1], con_details[2], con_details[3]):
        return False
    
    if get_meta("configured") == "true":
        return True
    else:
        return False