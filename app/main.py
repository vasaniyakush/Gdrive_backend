from fastapi import Body, FastAPI, Depends, HTTPException,status


from .Routers import files,folders



#-----------------------------------DATABASE CREATION----------------------------
# models.Base.metadata.create_all(bind=engine) #we dont need this because now we use alembic 
                                                #for table creation

app = FastAPI()
app.include_router(files.router)
app.include_router(folders.router)




