from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore


DB_URL ="mysql+pymysql://root:mysql1234@localhost:3306/mydb"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit = False,autoflush = False ,bind = engine)