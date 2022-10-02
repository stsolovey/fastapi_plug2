import string

from user import get_uid_by_token
from data import execute_query
from Levenshtein import distance

def translate(token, exercise_id, translation_from_user):

    user_id = get_uid_by_token(token)
    if user_id == None:
        d = {}
        d['message']='you should login first'
        d['goto']='login'

        return d
    
    # todo: check if there is an exercise with such an id and a user_id waiting for an anwser

    exercise_row = get_exercise_by_id(exercise_id)

   

    if exercise_row == []:
        return {'message':'no such exercise', 'togo':'exercise'}

    if exercise_row[0][5] !=None:
        return {'message':'the exercise has already been completed', 'togo':'exercise'}


    
    
    sentence_id = get_sentence_id_by_exercise_id(exercise_id)

    sentence_row = get_sentence_by_id(sentence_id)

    sentence = sentence_row[0][1]
    translation_from_database = sentence_row[0][2]

    result = check_answer(translation_from_database, translation_from_user)

    created, answered = write_result_to_exercises_table(exercise_id, result)[0]



    d = {}
    d['sentence'] = sentence
    d['translation'] = translation_from_database
    d['answer'] = translation_from_user
    d['distanse'] = result
    d['time'] = answered-created

    if result == 0:
        d['comment'] = "Great!"
    elif result == 1:
        d['comment'] = "Great! You made a small typo."
    elif result == 2:
        d['comment'] = "Not bad! But you made typos."
    elif  result > 2:
        d['comment'] = "We expected different answer."

    return d

def get_sentence_id_by_exercise_id(exercise_id):
    query = """
    SELECT sentence_id FROM exercises WHERE exercise_id = {};
    """.format(exercise_id)

    return execute_query(query)[0][0]

def get_sentence_by_id(sentence_id):
    query = """
    SELECT * FROM sentences WHERE sentence_id = {};
    """.format(sentence_id)

    return  execute_query(query)

def check_answer(translation_from_database, translation_from_user):
    
    t1 = translation_from_database.lower().translate(str.maketrans('', '', string.punctuation))
    t2 = translation_from_user.lower().translate(str.maketrans('', '', string.punctuation))

    t1 = " ".join(t1.split())
    t2 = " ".join(t2.split())

    result = distance(t1, t2)

    return result

def write_result_to_exercises_table(exercise_id, result):
    short_flag = False
    if result<=2:
        short_flag = True

    query = """
    UPDATE exercises
        SET answered = NOW(),
        result = {}
        WHERE exercise_id = {} RETURNING created, answered;
    """.format(short_flag, exercise_id)

    returning = execute_query(query)

    return returning

def is_there_an_active_exercise(exercise_id):
    query = """
    SELECT * FROM exercises WHERE exercise_id = '{}';
    """.format(exercise_id)

    result = execute_query(query)
    if result == []:
        return False
    if result == False:
        return False
    if execute_query(query)[0][5]!= None:
        return False
    return True

def get_exercise_by_id(exercise_id):
    query = """
    SELECT * FROM exercises WHERE exercise_id = '{}';
    """.format(exercise_id)

    result = execute_query(query)
 
    return result
