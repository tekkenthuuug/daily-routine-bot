from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base
from dataclasses import dataclass
import datetime


@dataclass
class UserTask(Base):
    __tablename__ = 'userTask'

    id: int = Column(Integer, primary_key=True)
    tg_user_id: int = Column(Integer)
    description: str = Column(String)
    completed: bool = Column(Boolean)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
