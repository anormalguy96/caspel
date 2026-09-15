from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

api = FastAPI()

users = {
    1: {"name": "Əli", "age": 23},
    2: {"name": "Vəli", "age": 24},
    3: {"name": "Xədicə", "age": 22},
    4: {"name": "Kamil", "age": 29},
}

items = {
    1: {"name": "Notebook"},
    2: {"name": "Phone"},

}

@api.get("/")
def main():
    return {"message": "FastAPI işləyir"}

@api.get("/users/search")
def search_user(q: str = None, limit: int = 10):
    if q:
        needed_user = [user for user in users.values() if q.lower() in user["name"].lower()]
    else:
        needed_user = list(users.values())
    
    return needed_user[:limit]

@api.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users.keys():
        raise HTTPException(
            status_code=404,
            detail="İstifadəçi tapılmadı"
        )
    return users[user_id]

@api.post("/users")
def create_user(user: User):
    new_id = max(users.keys(), default=0) + 1
    users[new_id] = user.model_dump()
    return {
        "message": "İstifadəçi yaradıldı",
        "user": users[new_id],
        "user_id": new_id
    }

@api.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    if user_id not in users.keys():
        raise HTTPException(
            status_code=404,
            detail="İstifadəçi tapılmadı"
        )
    users[user_id] = updated_user.model_dump()
    return {
        "message": "İstifadəçi yeniləndi",
        "user_id": user_id,
        "updated_user": updated_user.model_dump()
    }

@api.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users.keys():
        raise HTTPException(
            status_code=404,
            detail="İstifadəçi tapılmadı"
        )
    del users[user_id]
    return {
        "message": "İstifadəçi silindi",
        "user_id": user_id
    }

@api.get("/items/{item_id}")
def get_item(item_id: int, q: str = None):
    if item_id not in items.keys():
        raise HTTPException(
            status_code=404,
            detail="Əşya tapılmadı"
        )
    return items[item_id]
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="127.0.0.1", reload=True)