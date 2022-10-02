from conn import conn


def execute_query(query):

    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    return result

def get_categories():
    query = 'SELECT * FROM categories'
    
    cursor = conn.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.close()

    #rs = json.dumps(dict(records), ensure_ascii=False)
    return dict(records)



def get_sentences(limit, offset):
    query = 'SELECT sentence, translation FROM sentences LIMIT {} OFFSET {}'.format(limit, offset)
    
    cursor = conn.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.close()

    #rs = json.dumps(dict(records), ensure_ascii=False)
    return dict(records)

def count_rows(table):
    query = 'SELECT COUNT(*) FROM {}'.format(table)
    
    cursor = conn.cursor()
    cursor.execute(query)
    number = cursor.fetchall()[0][0]
    cursor.close()

    return number