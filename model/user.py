from sqlalchemy import Column, Integer, DateTime
from database import Base
import datetime

class User(Base):
    __tablename__ = 'user'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    tg_user_id: int = Column(Integer, primary_key=True, unique=True)
    utc_offset: int = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
