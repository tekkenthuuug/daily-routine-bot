from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class UserTask(Base):
    __tablename__ = 'userTask'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    description = Column(String)
    completed = Column(Boolean)

    def __repr__(self):
        return "<UserTask(%r, %r)>" % (
            self.description, self.completed
        )