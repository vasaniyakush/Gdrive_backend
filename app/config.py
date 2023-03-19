from pydantic import BaseSettings

from app import database
class Settings(BaseSettings): #this will automatically 
                            #import values from environmnet varuiables which
                            # have the same name
    database_hostname: str = ""
    database_port: str = ""
    database_password: str = ""
    database_gdrive: str = ""
    database_username: str = ""
    class Config:
        env_file = ".env"

settings = Settings()