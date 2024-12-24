from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends

user_pgsql_url = 'mysql+pymysql://jonnyan404:www.mrdoc.fun@172.31.22.85:3306/mrdoc'
user_connect_args = {"check_same_thread": False}
user_engine = create_engine(user_pgsql_url, connect_args=user_connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(user_engine)


def get_session():
    with Session(user_engine) as user_session:
        yield user_session


UserSessionDep = Annotated[Session, Depends(get_session)]
