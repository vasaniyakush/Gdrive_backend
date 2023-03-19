from multiprocessing import synchronize
from tkinter.messagebox import NO
from urllib import response
from fastapi import APIRouter, Body, FastAPI, Depends, HTTPException,status
from urllib.parse import urlparse
from urllib.parse import parse_qs
from sqlalchemy.orm import Session
from .. import models
from .. import schemas
from ..database import  get_db

router = APIRouter(prefix="/file",tags=["Files"])


@router.get("/")
def getFile(db:Session = Depends(get_db),location:str = "/",name:str =""):
    url = location
    file_name = name
    actual_loc = url
    if location[-1] != "/":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"something looks wrong with location: {location} or name: {name}. Please check")
    content = db.query(models.File).filter(models.File.location == actual_loc, models.File.name == file_name).first()
    if content is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No such file was found. Location: {location}, Name: {name}")
    return content

@router.post("/",response_model=schemas.FileResponse,status_code=status.HTTP_201_CREATED)
def createFile(newfile:schemas.FileCreate,db:Session = Depends(get_db)):
    if newfile.location[-1] != "/":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"something looks wrong with location: {newfile.location}. Please check")
    
    if newfile.location == "/":
        checkfile = db.query(models.File).filter(models.File.location == f"{newfile.location}", models.File.name == newfile.name).first()
        if checkfile is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="File with same name exists")
        new_file = models.File(**newfile.dict(), folder_id = 0)
    else:
        folders = newfile.location.split('/')
        folder_loc = "/"
        # print(folders[:-2])
        for i in folders[1:-2]:
            # print(i)
            folder_loc += i+"/"
        folder_name = folders[-2]
        print(folder_loc, "folder_loc")
        print(folder_name, "folder_name")
        print(newfile.location)
        checkfile = db.query(models.File).filter(models.File.location == f"{newfile.location}", models.File.name == newfile.name).first()
        if checkfile is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="File with same name exists")
        folder_id_get = db.query(models.Folder).filter(models.Folder.location == folder_loc, models.Folder.name == folder_name).first()

        new_file = models.File(**newfile.dict(), folder_id = folder_id_get.id)
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
 
    return new_file

@router.delete("/",status_code=status.HTTP_204_NO_CONTENT)
def deleteFile(file:dict = Body(...),db: Session = Depends(get_db)):
    print(file.get("location"))
    print(file.get("name"))
    delete_query = db.query(models.File).filter(models.File.location == file.get("location"),models.File.name == file.get("name") )
    delete_obj = delete_query.first()
    if delete_obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not found")   
    delete_query.delete(synchronize_session = False)
    db.commit()
    return {"message":"File was deleted"}

@router.put("/",response_model=schemas.FileResponse)
def renameFile(newfile:schemas.fileUpdate,db:Session = Depends(get_db)):
    print(newfile.location)
    checkfile = db.query(models.File).filter(models.File.location == newfile.location,models.File.name == newfile.newName).first()
    print(checkfile)
    if checkfile is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="File with same name exists")
    print(newfile.location)
    update_query= db.query(models.File).filter(models.File.location == newfile.location,models.File.name == newfile.oldName)
    print(update_query.first())
    # new_File = schemas.FileCreate({content=})
    update_query.update({"name":f"{newfile.newName}"},synchronize_session=False)
    db.commit()
    new_file = db.query(models.File).filter(models.File.location == newfile.location, models.File.name == newfile.newName).first()
    return new_file
    

# /
# folder1 folder2 folder3    #get data of this folder #update breadcrub
# #get data of this folder
# -location = current breadcrumb
# -name = folder1
# # update breadcrub
# -current br + foldername + "/"

# /folder1/
# folder3 folder4
# #get data of this folder
# -location = current breadcrumb
# -name = folder3
# # update breadcrub
# -current br + foldername + "/"
# /folder1/folder3/
# #go back
# #update breadcrumb
# remove "/", remove folder
# /folder1/
# -location - "/"
# -name = folder1



