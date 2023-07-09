from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///DataBase/vac_db.db')
Base = declarative_base()




class Vacancies(Base):
    __tablename__ = 'vacancies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company = Column(String, nullable=False)
    name = Column(Integer, nullable=False)
    url = Column(Integer, nullable=False)
    parse_time = Column(DateTime, nullable=False)
    status = Column(Integer, nullable=False)


Base.metadata.create_all(engine)
