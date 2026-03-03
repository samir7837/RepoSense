from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base


class Repository(Base):

    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)

    github_id = Column(String, index=True)

    repo_name = Column(String)

    full_name = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))