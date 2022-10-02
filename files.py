from fastapi import File, UploadFile
from datetime import datetime
from fastapi.responses import FileResponse


def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        filename = 'uploads/' + datetime.now().strftime("%m-%d-%Y_%H-%M-%S,%f_") + file.filename
        with open(filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}

def download(filename):
    path_to_files = 'files/'
    file_path = path_to_files+filename
    return FileResponse(path=file_path, filename=file_path, media_type='application/zip')