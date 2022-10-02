import psycopg2

from conf import HOST, PORT, DBNAME, USER, PASSWORD 

conn = psycopg2.connect("""
    host={}
    port={}
    dbname={}
    user={}
    password={}
    target_session_attrs=read-write
    sslmode=verify-full
""".format(HOST, PORT, DBNAME, USER, PASSWORD))

conn.autocommit = True