from re import sub
from tkinter import N
from tkinter.messagebox import NO
from typing import List
from unicodedata import name
from fastapi import APIRouter, Body, FastAPI, Depends, HTTPException, status
from urllib.parse import urlparse
from urllib.parse import parse_qs
from sqlalchemy.orm import Session
from .. import models
from .. import schemas
from ..database import get_db

router = APIRouter(prefix="/folder", tags=["Folders"])


@router.get("/", response_model=schemas.folderContents)
def getFolders(db: Session = Depends(get_db), location: str = "", name: str = ""):
    all_folders = ""
    all_files = ""
    if location == "/":
        if name == "":
            print("if if")
            all_folders = (
                db.query(models.Folder).filter(models.Folder.location == f"/").all()
            )
            all_files = db.query(models.File).filter(models.File.location == "/").all()
        else:
            actual_loc = location
            print(f"/+{name}", "if else")
            all_folders = (
                db.query(models.Folder)
                .filter(models.Folder.location == f"/{name}/")
                .all()
            )
            all_files = (
                db.query(models.File).filter(models.File.location == f"/{name}/").all()
            )

    else:
        actual_loc = location
        all_folders = (
            db.query(models.Folder)
            .filter(models.Folder.location == f"{actual_loc}{name}/")
            .all()
        )
        all_files = (
            db.query(models.File)
            .filter(models.File.location == f"{actual_loc}{name}/")
            .all()
        )

    return {"folders": all_folders, "files": all_files}


@router.post("/", status_code=status.HTTP_201_CREATED)
def createFolders(newFolder: schemas.FolderCreate, db: Session = Depends(get_db)):
    folder = (
        db.query(models.Folder)
        .filter(
            models.Folder.name == newFolder.name,
            models.Folder.location == newFolder.location,
        )
        .first()
    )
    if folder is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Duplicate folder"
        )
    new_Folder = models.Folder(**newFolder.dict())
    db.add(new_Folder)
    db.commit()
    db.refresh(new_Folder)
    return new_Folder


# to delete a folder, delete all the files and folders with location prefix as location of deleting folder


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT )
def deleteFolder(folder: schemas.FolderDelete, db: Session = Depends(get_db)):
    print(folder.dict(), "here1")
    folder_query = (
        db.query(models.Folder)
        .filter(
            models.Folder.name == folder.name, models.Folder.location == folder.location
        )
        .first()
    )
    if folder_query is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Folder with location: {folder.location} and name: {folder.name} not found",
        )
    print(folder.dict(), "here2")
    # folder_id = db.query(models.Folder).filter(models.Folder.name == folder.name, models.Folder.location == folder.location).first().id
    subfolder_loc = "{}%".format(folder.location + folder.name + "/")
    folder_loc = "{}%".format(folder.location)
    print(subfolder_loc)
    print(folder_loc)
    child_folders = (
        db.query(models.Folder)
        .filter(models.Folder.location.ilike(subfolder_loc))
        .all()
    )
    child_folder = (
        db.query(models.Folder)
        .filter(models.Folder.location.ilike(folder_loc), models.Folder.name==folder.name)
        .all()
    )
    
    child_files = (
        db.query(models.File).filter(models.File.location.ilike(subfolder_loc)).all()
    )
    print(child_files)
    print(child_folders)
    print(child_folder)
    db.query(models.Folder).filter(models.Folder.location.ilike(subfolder_loc)).delete()
    db.query(models.Folder).filter(models.Folder.location.ilike(folder_loc), models.Folder.name==folder.name).delete()
    db.query(models.File).filter(models.File.location.ilike(subfolder_loc)).delete()

    db.commit()
    # print(child_folders)
    # return {"files":child_files,"folders":child_folders,"folder":child_folder}

@router.put("/",response_model=schemas.FolderResponse)
def renameFolder(folder: schemas.FolderUpdate, db:Session = Depends(get_db)):
    get_folder = db.query(models.Folder).filter(models.Folder.location == folder.location, models.Folder.name == folder.newName).first()
    if get_folder is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Folder with name {folder.newName} already exists")

    get_folder = db.query(models.Folder).filter(models.Folder.location == folder.location, models.Folder.name == folder.oldName).first()
    if get_folder is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Folder with location: {folder.location} and name: {folder.oldName} does not exist")
    sub_loc = "{}%".format( f"{folder.location}{folder.oldName}/")
    len_of_folderloc = len(folder.location.split("/")) - 1
    print(len_of_folderloc, "len_of)loc")
    print(sub_loc, "sub_loc")
    get_folder_list = db.query(models.Folder).filter(models.Folder.location.ilike( sub_loc)).all()
    for fldr in get_folder_list:
        loc = fldr.location
        separated_location = loc.split("/")
        print(separated_location , "separated_location")
        separated_location[len_of_folderloc] = folder.newName
        print(separated_location , "separated_location_changed")
        loc = ""
        for i in separated_location[:-1]:
            loc += i+"/"
        print(loc, "loc")
        db.query(models.Folder).filter(models.Folder.id == fldr.id).update({"location":loc},synchronize_session=False)
        db.commit()
    
    print(len_of_folderloc, "len_of)loc")
    print(sub_loc, "sub_loc")
    get_file_list = db.query(models.File).filter(models.File.location.ilike( sub_loc)).all()
    for fl in get_file_list:
        print(fl)
        loc = fl.location
        separated_location = loc.split("/")
        print(separated_location , "separated_location")
        separated_location[len_of_folderloc] = folder.newName
        print(separated_location , "separated_location_changed")
        loc = ""
        for i in separated_location[:-1]:
            loc += i+"/"
        print(loc, "loc")
        db.query(models.File).filter(models.File.id == fl.id).update({"location":loc},synchronize_session=False)
        db.commit()
    update_query= db.query(models.Folder).filter(models.Folder.id == get_folder.id)
    # print(update_query.first())
    update_query.update({"name":f"{folder.newName}"},synchronize_session=False)
    db.commit()
    get_folder = db.query(models.Folder).filter(models.Folder.name == folder.newName, models.Folder.location==folder.location).first()
    return get_folder
    

    