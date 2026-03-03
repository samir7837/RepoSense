from sqlalchemy import Column, Integer, String, ForeignKey, Text
from app.db.database import Base


class Review(Base):

    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    repo_name = Column(String, index=True)

    file_name = Column(String)

    score = Column(Integer)

    review = Column(Text)

    github_id = Column(String, index=True)