import email
from secrets import token_bytes
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional, List



#---------------------USER--------------------------------------------------------
class FolderCreate(BaseModel):
    location: str
    name: str
    # password: str

class FolderResponse(BaseModel):
    id: int
    name: str
    location: str
    class Config:  #this sets the sqlalchemy model to be recongnised by pydantic model
        orm_mode = True
class FolderDelete(FolderCreate):
    pass
class FolderUpdate(BaseModel):
    location: str
    oldName: str
    newName: str


class FileCreate(BaseModel):
    name: str
    content: str
    location: str
    

class FileResponse(BaseModel):  
    name: str
    content: str
    location: str
    id: int
    folder_id: int
    folder: FolderResponse
    class Config:  #this sets the sqlalchemy model to be recongnised by pydantic model
        orm_mode = True
class folderContents(BaseModel):
    folders: List[FolderResponse]
    files:List[FileResponse]
class fileUpdate(BaseModel):
    location: str
    oldName: str
    newName: str
    class Config:
        orm_mode = True

# class PostOut(BaseModel):
#     Post: PostResponse
#     votes: int
#     class Config:  #this sets the sqlalchemy model to be recongnised by pydantic model
#         orm_mode = True

#--------------------LOGIN----------------------------------------------------------

