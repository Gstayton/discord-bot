from sqlalchemy import Column, ForeignKey, VARCHAR, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import config

import logging
log = logging.getLogger(__name__)

S = sessionmaker()

Base = declarative_base()

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
S.configure(bind=engine)

session = S()
def get_session() -> Session:
    return session

class PSO2User(Base):
    __tablename__ = "PSO2Users"

    user_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(VARCHAR, primary_key=True, nullable=False)
    player_id = Column(VARCHAR, primary_key=True, nullable=False)
    timezone = Column(VARCHAR(64), nullable=True)

    def __repr__(self):
        return f"<User(user_id={self.user_id}, username={self.username}, player_id={self.player_id})>"

Base.metadata.create_all(engine)
