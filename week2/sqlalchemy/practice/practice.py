import sqlalchemy as sa
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker



# creating engine in memory
engine = create_engine("postgresql://postgres:35623346@localhost:5432/caspel_ai")
# for sqlite ->  "sqlite:///:memory:"
# for mysql -> "mysql+pymysql://username:password@host:port/database"

session = sessionmaker(bind=engine)
conn = engine.connect()

# creating metadata
metadata = MetaData() 

# creating table users
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("age", Integer),
)


def insert_user(name, age):
    conn.execute(users.insert(), {
        "name": name, 
        "age": age
    })

def get_user(user_id):
    return conn.execute(users.select().where(users.c.id == user_id)).fetchone()

def get_users():
    return conn.execute(users.select()).fetchall()

def update_user(user_id, name, age):
    conn.execute(users.update().where(users.c.id == user_id), {
        "name": name, 
        "age": age
    })

def delete_user(user_id):
    conn.execute(users.delete().where(users.c.id == user_id))

metadata.create_all(engine)

print(users.select())
print(users.insert())
print(users.update())
print(users.delete())

print("Inserting user 1: ", insert_user("Ilkin", 25))
print("Inserting user 2: ", insert_user("Veli", 24))
print("Inserting user 3: ", insert_user("Vusal", 26))
print("All users: ", get_users())
print("Updating user 1: ", update_user(1, "Ali", 26))
print("After updating user 1: ", get_users())
print("Deleting user 1: ", delete_user(1))
print("After deleting user 1: ", get_users())