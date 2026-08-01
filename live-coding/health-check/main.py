from fastapi import FastAPI

app = FastAPI()


# ✅ The heartbeat — no logic, no auth, no database. Just a pulse.
@app.get("/health")
async def health():
    return {"status": "ok"}


# 🧠 A real endpoint — has business logic, can fail for many reasons
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # Simulate a database lookup
    fake_db = {1: "Mo", 2: "Sara", 3: "Ali"}
    if user_id not in fake_db:
        return {"error": "User not found"}
    return {"id": user_id, "name": fake_db[user_id]}
