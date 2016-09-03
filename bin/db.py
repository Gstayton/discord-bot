from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import config

Session = sessionmaker()

Base = declarative_base()

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
Session.configure(bind=engine)

session = Session()


class Server(Base):
    __tablename__ = "servers"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    server_id = Column(Integer, unique=True, nullable=False)

    users = relationship("User", backref='server', lazy='dynamic')

    def __repr__(self):
        return "Server id: {} / Server Name: {}".format(
            self.server_id,
            self.name
        )


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, unique=True)
    username = Column(String(250))
    role_set = Column(Boolean, default=True)

    server_id = Column(Integer, ForeignKey('servers.id'), nullable=False)

    def __repr__(self):
        return "User id: {} / User Name: {}".format(
            self.user_id,
            self.username
        )

Base.metadata.create_all(engine)
