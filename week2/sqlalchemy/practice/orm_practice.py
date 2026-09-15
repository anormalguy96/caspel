from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, URL
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(ENV_PATH)


url = URL.create(
    "postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host="localhost",
    port=5432,
    database=os.getenv("DB_NAME")
)
engine = create_engine(url)
session = sessionmaker(bind=engine)
session = session()

# User ORM model

class Base(DeclarativeBase):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    email = Column(String)
    is_active = Column(Boolean)
    created_at = Column(DateTime)

# mapped + mapped column


# inserting
session.add_all([
    Student(name="Ilkin", age=25, email="[EMAIL_ADDRESS]", is_active=True, created_at=datetime.now()),
    Student(name="Veli", age=24, email="[EMAIL_ADDRESS]", is_active=True, created_at=datetime.now()),
    Student(name="Vusal", age=26, email="[EMAIL_ADDRESS]", is_active=True, created_at=datetime.now()),
])
session.commit()

# getting
students = session.scalars(select(Student)).all()
print(students)

# updating
session.execute(
    update(Student).where(Student.id == 1).values({
        "name": "Ilkin",
        "age": 26,
        "email": "[EMAIL_ADDRESS]",
        "is_active": True,
        "created_at": datetime.now()
    })
)
session.commit()

# updating
session.query(Student).filter(Student.id == 1).update({
    "name": "Ilkin",
    "age": 26,
    "email": "[EMAIL_ADDRESS]",
    "is_active": True,
    "created_at": datetime.now()
})
session.commit()

# deleting
session.query(Student).filter(Student.id == 1).delete()
session.commit()
