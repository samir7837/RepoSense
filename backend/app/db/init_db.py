from app.db.database import engine, Base

from app.models.user import User
from app.models.repository import Repository


def init_db():

    Base.metadata.create_all(bind=engine)