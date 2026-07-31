from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


# ❌ The broken version — accepts literally anything
@app.post("/create-user-bad")
async def create_user_bad(data: dict):
    return {"saved": data}


# ✅ The fixed version — Pydantic enforces the contract
class User(BaseModel):
    name: str
    email: EmailStr


class UserResponse(BaseModel):
    name: str
    email: str


@app.post("/create-user", response_model=UserResponse)
async def create_user(user: User):
    # Simulate saving to DB — in reality this would have more fields (id, password hash, etc.)
    internal_data = {
        "name": user.name,
        "email": user.email,
        "password_hash": "hashed_secret_123",
        "internal_id": 42,
    }
    return internal_data
