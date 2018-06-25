from sqlalchemy import Column, Integer, String
from .config import Base


class Cat(Base):
    __tablename__ = 'cats'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
