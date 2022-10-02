from conn import conn
import hashlib
import string
import random

def add_user(login, password):
    message = 'login {} is already taken'.format(login)
    answer = {'status':False,'message':message}
    if check_login_if_exists(login):
        return answer

    message = 'password is too short'
    answer = {'status':False,'message':message}
    if password == '':
        return answer
    
    token = (random_string(190))
    hpass = hashpassword(password)
    
    query = """
    INSERT INTO users (login, password, token) VALUES('{}', '{}', '{}');
    """.format(login, hpass, token)
    
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()
    
    return {'status':True,'token':token}

def autorisation(login, password):
    message = 'login or password is incorrect'
    answer = {'status':False,'message':message}
    
    if check_login_if_exists(login)==False:
        return answer
    
    if check_login_and_password_mach(login, password)==False:
        return answer
    
    token = (random_string(190))
    
    query = """
    UPDATE users
    SET token = '{}',
    timetag = NOW()
    WHERE login='{}';
    """.format(token, login)
    
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()
    
    return {'status':True,'token':token}

    
def check_login_if_exists(login):
    cursor = conn.cursor()
    
    query = """
    SELECT EXISTS(SELECT 1 FROM users WHERE login = '{}');
    """.format(login)
    
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    return result[0][0]

def check_login_and_password_mach(login, password):
    cursor = conn.cursor()
    hpass = hashpassword(password)
    
    query = """
    SELECT EXISTS(SELECT 1 FROM users WHERE login = '{}' AND password = '{}');
    """.format(login, hpass)
    
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    return result[0][0]

def random_string(length):
    return "=="+''.join(random.choice(string.ascii_letters) for m in range(length))+"=="

def hashpassword(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()