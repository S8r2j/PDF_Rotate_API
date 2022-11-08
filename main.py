from fastapi import FastAPI,UploadFile,File
from fastapi.responses import FileResponse
import shutil
import pikepdf

app=FastAPI()


@app.post("/api/file")
async def get_file(angle_of_rotation:int,page_number:int,file:UploadFile=File(...)):
    with open(f"{file.filename}","wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
    old_file=pikepdf.Pdf.open(f"{file.filename}")
    global file_name
    file_name=file.filename
    count=1
    for i in old_file.pages:
        if(count==page_number):
            i.Rotate=angle_of_rotation
            old_file.save(f"tmp/{file.filename}")
            break
        count=count+1
    return {"file_url":f"localhost:8000/api/{file_name}"}


@app.get("/api/{convert_file_name}")
async def get_file(convert_file_name:str):
    return FileResponse(f"tmp/{convert_file_name}")