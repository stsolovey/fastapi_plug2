from conn import conn
from data import count_rows, execute_query
from user import get_uid_by_token

from random import randrange

def get_exercise(token):
    user_id = get_uid_by_token(token)
    if user_id==None:
        return {'status':False, 
        'message':'you should login first', 
        'togo':'/login', 
        'expected':'token'}

    range = count_rows('sentences')+1

    query = """
    SELECT sentence_id, sentence FROM sentences LIMIT 1 OFFSET {};
    """.format(randrange(start=1, stop=range))
    
    result = execute_query(query)

    sentence_id = result[0][0]
    sentence = result[0][1]
    
    id_of_new_exercise = create_new_exercise(user_id, sentence_id)
    
    d = {'status': True}
    d['exercise_id'] = id_of_new_exercise
    d['sentence'] = sentence 

    
    return d

def create_new_exercise(user_id, sentence_id):
       
    query = """
    INSERT INTO exercises (user_id, sentence_id) VALUES('{}', '{}') RETURNING exercise_id;
    """.format(user_id, sentence_id)

    cursor = conn.cursor()
    cursor.execute(query)
    id_of_new_exercise = cursor.fetchone()[0]
    cursor.close()

    return id_of_new_exercise
    
