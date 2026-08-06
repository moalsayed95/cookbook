from fastapi import FastAPI, HTTPException, status

app = FastAPI()

USERS = {
    1: {"id": 1, "name": "Mo"},
    2: {"id": 2, "name": "Sara"},
    3: {"id": 3, "name": "Ali"},
}


# ❌ The client receives 200 OK + null when the user does not exist.
@app.get("/users-bad/{user_id}")
async def get_user_bad(user_id: int):
    return USERS.get(user_id)


# ✅ The status code and response body both describe what happened.
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = USERS.get(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user
