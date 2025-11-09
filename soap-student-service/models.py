from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from database import engine


Base = declarative_base()
SessionLocal = sessionmaker(bind = engine)

class StudentMetadata(Base):
    __tablename__ = "student_metadata"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String)
    age = Column(Integer)
    department = Column(String)
    
# Create table if not exists
Base.metadata.create_all(engine)