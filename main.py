from fastapi import FastAPI, UploadFile, File

app = FastAPI(title="Load Testing Plug")

import auth, data, exercise, files, translate as tr

@app.get("/")
async def index():
    print ("function name: ", index.__name__)
    item = {'Available options': ['register', 'login', 'download', 'upload', 'categories', 'sentences', 'exercise', 'translate']}
    return item

@app.get("/register")
async def register(login: str | None = None, password: str| None = None):
    if login==None or password==None:
        return {"message": "login and password required"}
    else:
        return auth.add_user(login, password)

@app.get("/login")
async def login(login: str | None = None, password: str | None = None):
    if login==None or password==None:
        return {"message": "login and password required"}
    else:
        return auth.autorisation(login, password)

@app.get("/download")
def download(filename: str | None = None):
    if filename == None:
        return {'message':'filename required'}
    else:
        return files.download(filename)

@app.post("/upload")
def upload(file: UploadFile = File(...)):
    return files.upload(file)

@app.get("/categories")
async def categories():
    return data.get_categories()

@app.get("/sentences")
async def sentences(limit: int = 200, offset: int = 0):
    print ("function name: ", sentences.__name__)
    return data.get_sentences(limit, offset)

@app.get("/exercise")
async def get_exercise(token: str | None = None):
    if token == None:
        return {'message':'you should login first', 'togo':'/login', 'expected':'token'}
    else:
        return exercise.get_exercise(token)

@app.get("/translate")
async def translate(token: str,  exercise_id: int, translation: str):
    print ("function name: ", translate.__name__)
    return tr.translate(token,  exercise_id, translation)