

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
# from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
# from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
class File(Base):
    __tablename__ = "file"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    content = Column(String, nullable=False)
    location = Column(String,nullable=False)
    folder_id = Column(Integer, ForeignKey("folder.id",ondelete="CASCADE"), nullable=False)   
    folder = relationship("Folder") #this also returns a User property based off owner_id using foreignkey
    # published = Column(Boolean,server_default='TRUE' , nullable=False)
    # created_at = Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))

class Folder(Base):
    __tablename__ = "folder"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)

    location = Column(String,nullable=False)
   