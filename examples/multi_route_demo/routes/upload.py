from fastapi import APIRouter, UploadFile, File
from typing import List

router = APIRouter()

@router.post("/file/")
async def create_file(file: UploadFile = File(...)):
    file_contents = await file.read()
    return {"filename": file.filename, "file_size": len(file_contents)}

@router.post("/files/")
async def create_files(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        contents = await file.read()
        results.append({"filename": file.filename, "file_size": len(contents)})
    return results