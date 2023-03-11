from typing import List
from fastapi import APIRouter, Body, FastAPI, Depends, HTTPException,status
from urllib.parse import urlparse
from urllib.parse import parse_qs
from sqlalchemy.orm import Session
from .. import models
from .. import schemas
from ..database import  get_db

router = APIRouter(prefix="/folder",tags=["Folders"])


@router.get("/",response_model=schemas.folderContents)
def getFolders(loc:dict = Body(...),db:Session = Depends(get_db)):
    # print(loc.get("location"))
    # print("hello")
    # print(loc)
    all_folders = ""
    all_files = ""
    url = urlparse(loc.get("location"))
    # print(url.path)
    if url.path == "/":
        # print("in here")
        if url.query == "": 
            print("if if")
            all_folders = db.query(models.Folder).filter(models.Folder.location == f'/').all()
            all_files = db.query(models.File).filter(models.File.location == "/").all()
        else:
            name = parse_qs(url.query)["name"][0]
            actual_loc = url.path
            print(f"/+{name}" , "if else")
            all_folders = db.query(models.Folder).filter(models.Folder.location == f'/{name}/').all()
            all_files = db.query(models.File).filter(models.File.location == f"/{name}/").all()

    else:
        name = parse_qs(url.query)["name"][0]
        # print(name)
        actual_loc = url.path
        # print(actual_loc)
        # print(db.query(models.Folder).all())
        # print(f'{actual_loc}/{name}/')
        all_folders = db.query(models.Folder).filter(models.Folder.location == f'{actual_loc}/{name}/').all()
        all_files = db.query(models.File).filter(models.File.location == f"{actual_loc}/{name}/").all()
        # print(all_folders)
    # print("hello")
    return {"folders":all_folders,"files":all_files}
    
@router.post("/",status_code=status.HTTP_201_CREATED)
def createFolders(newFolder: schemas.FolderCreate,db:Session = Depends(get_db)):
    folder = db.query(models.Folder).filter(models.Folder.name == newFolder.name,models.Folder.location == newFolder.location).first()
    if folder is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail=f"Duplicate folder")
    new_Folder = models.Folder(**newFolder.dict()) 
    db.add(new_Folder )
    db.commit()
    db.refresh(new_Folder)
    return new_Folder

# to delete a folder, delete all the files and folders with location prefix as location of deleting folder

