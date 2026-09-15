from sqlalchemy import create_engine, text, URL, MetaData, Table, Column, Integer, String, Boolean, DateTime
from dotenv import load_dotenv
from pathlib import Path
import os
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = int(os.getenv("DB_PORT"))
db_name = os.getenv("DB_NAME")
if not db_user or not db_password or not db_host or not db_port or not db_name:
    print("Verilənlərdən biri və ya bir neçəsi yoxdur")
    exit()

url = URL.create(
    "postgresql+psycopg",
    username=db_user,
    password=db_password,
    host=db_host,
    port=db_port,
    database=db_name
)
engine = create_engine(url)
connect = engine.connect()

metadata = MetaData()
metadata.create_all(engine)

try:
    connect.execute(text("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50),
            email VARCHAR(255),
            age INTEGER,
            is_active BOOLEAN,
            created_at TIMESTAMP
        );
    """))
except Exception as e:
    print(e)

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('email', String),
    Column('age', Integer),
    Column('is_active', Boolean),
    Column('created_at', DateTime)
)

# inserting
connect.execute(users.insert().values({
    'name': 'Samir',
    'email': 'samir123@gmail.com',
    'age': 24,
    'is_active': True,
    'created_at': datetime.now()
},
{
    'name': 'Nurlan',
    'email': 'nurlan123@gmail.com',
    'age': 19,
    'is_active': True,
    'created_at': datetime.now() + timedelta()
},
{
    'name': 'Nihad',
    'email': 'nihad123@gmail.com',
    'age': 30,
    'is_active': True,
    'created_at': datetime.now()+timedelta(days=2)
},
{
    'name': 'Fidan',
    'email': 'fidan12@gmail.com',
    'age': 23,
    'is_active': True,
    'created_at': datetime.now()+timedelta(hours=3)
},
{
    'name': 'Gunay',
    'email': 'gunay123@gmail.com',
    'age': 21,
    'is_active': True,
    'created_at': datetime.now()+timedelta(minutes=4)
}
))

# updating
connect.execute(users.update().where(users.c.name == 'Ilkin').values({
    'age': 26
}))

# deleting
connect.execute(users.delete().where(users.c.name == 'Ilkin'))