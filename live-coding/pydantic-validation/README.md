# Pydantic Validation — The Bouncer Your API Is Missing

Your endpoint accepts a raw `dict`. That means someone can POST `"hello"` and your server says "cool, saved." Imagine that `"hello"` hitting your production database as a new user row.

One import fixes this. Pydantic turns your endpoint from an open door into a bouncer with a clipboard.

---

## The Idea

Without validation, your API is a mailbox with no slot — you can shove anything in: a letter, a pizza, a live raccoon. It all gets "delivered."

Here's the broken endpoint — it accepts a raw `dict`, which means literally anything:

```python
@app.post("/create-user-bad")
async def create_user_bad(data: dict):
    return {"saved": data}
```

Pydantic gives you a **contract**: a strict shape definition that says "I accept a `name` (string) and an `email` (valid email). Everything else gets rejected before your code even runs."

```python
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    email: EmailStr
```

That's it. That class is the bouncer. Now you swap the `dict` for `User` in the endpoint signature:

```python
@app.post("/create-user")
async def create_user(user: User):
    return {"name": user.name, "email": user.email}
```

| Without Pydantic | With Pydantic |
|---|---|
| Accepts any JSON — dicts, strings, garbage | Only accepts data matching your exact schema |
| You write `if` statements for every field | Validation is automatic + free |
| Bad data silently enters your DB | Bad data gets rejected with a clear 422 error |
| Response can accidentally leak internal fields | `response_model` controls exactly what goes out |

Think of it like a customs checkpoint at an airport:

- **No Pydantic** = no customs. Anyone walks through with anything. Contraband, expired passports, someone else's suitcase. All fine.
- **With Pydantic** = every piece of data shows its passport. Wrong format? Missing field? Invalid email? You're not getting through.

---

## How It Works

Here's what happens on every request to a Pydantic-protected endpoint:

1. Request arrives with a JSON body
2. FastAPI hands the body to Pydantic
3. Pydantic checks: does it match the model? Every field present? Correct types?
4. **Valid** → your function runs, response goes through `response_model` filter
5. **Invalid** → instant `422 Unprocessable Entity` with a detailed error. Your function never executes.

```
Without Pydantic:
  Client → POST {"garbage": true} → Server accepts it → DB saves garbage
  Client → POST "hello"           → Server accepts it → DB saves "hello"
  Client → POST {"name": "Mo"}    → Server accepts it → but where's the email?

With Pydantic:
  Client → POST "hello"           → 422: "value is not a valid dict"
  Client → POST {"garbage": true} → 422: "name: field required, email: field required"
  Client → POST {"name": "Mo", "email": "not-an-email"} → 422: "email: not a valid email"
  Client → POST {"name": "Mo", "email": "mo@dev.com"}   → ✅ 200 OK
```

Zero `if` statements. Zero manual checks. The contract enforces itself.

---

## The Second Superpower — Controlling What Goes Out

Validation isn't just about input. The `response_model` parameter controls what your API **sends back**.

Your internal `User` object might have a password hash, an internal ID, admin flags — fields that should never leave the server. Without `response_model`, one accidental `return user` leaks everything.

You create a second model — only the fields you want the outside world to see:

```python
class UserResponse(BaseModel):
    name: str
    email: str
```

Then tell FastAPI to use it as a filter:

```python
@app.post("/create-user", response_model=UserResponse)
async def create_user(user: User):
    # Internally we have password_hash, internal_id, etc.
    internal_data = {
        "name": user.name,
        "email": user.email,
        "password_hash": "hashed_secret_123",
        "internal_id": 42,
    }
    return internal_data  # FastAPI strips it down to only name + email
```

Even though the function returns 4 fields, the client only receives `name` and `email`. The `password_hash` and `internal_id` never leave the server. Zero accidental data leaks.

---

## Routes

| Method | Path | Auth required | Description |
|---|---|---|---|
| `POST` | `/create-user-bad` | No | The broken endpoint — accepts anything |
| `POST` | `/create-user` | No | The fixed endpoint — Pydantic-protected with `response_model` |

---

## Run

```bash
uv run uvicorn main:app --reload
```

---

## Test

Run these commands in order to see the difference between an unprotected and a protected endpoint.

**Step 1 — Send garbage to the unprotected endpoint:**

```bash
curl -s -X POST http://localhost:8000/create-user-bad \
  -H "Content-Type: application/json" \
  -d '"hello"'
```

Response: `{"saved": "hello"}` — it accepted a raw string as a "user." Your database just stored nonsense.

**Step 2 — Send the same garbage to the protected endpoint:**

```bash
curl -s -X POST http://localhost:8000/create-user \
  -H "Content-Type: application/json" \
  -d '"hello"'
```

Response: `422 Unprocessable Entity` — Pydantic rejected it instantly.

**Step 3 — Send a dict with missing fields:**

```bash
curl -s -X POST http://localhost:8000/create-user \
  -H "Content-Type: application/json" \
  -d '{"garbage": true}'
```

Response: `422` with errors telling you exactly what's wrong — `name` is required, `email` is required.

**Step 4 — Send an invalid email:**

```bash
curl -s -X POST http://localhost:8000/create-user \
  -H "Content-Type: application/json" \
  -d '{"name": "Mo", "email": "not-an-email"}'
```

Response: `422` — Pydantic knows `"not-an-email"` isn't a valid email address.

**Step 5 — Send valid data:**

```bash
curl -s -X POST http://localhost:8000/create-user \
  -H "Content-Type: application/json" \
  -d '{"name": "Mo", "email": "mo@sayeddev.com"}'
```

Response: `{"name": "Mo", "email": "mo@sayeddev.com"}` — only the fields declared in `UserResponse`. The `password_hash` and `internal_id` that exist internally? Stripped. Never sent to the client.

---

## In Production

This demo shows the core concept. In a real codebase you'd also use:

- **`Field()` validators** — min/max length, regex patterns, custom rules
- **Nested models** — `Address` inside `User` inside `Order`, all validated recursively
- **`Depends()`** — combine Pydantic validation with FastAPI's dependency injection for auth, DB sessions, etc.

Pydantic doesn't just validate — it's also the engine behind [Structured Output](../../topics/structured-output/) (forcing LLMs to return exact JSON schemas) and the reason [SQL Injection](../../topics/sql-injection/) becomes harder to pull off when you're never concatenating raw strings.

---

## TL;DR

Never accept a raw `dict` in a FastAPI endpoint. Define a Pydantic model — it's your contract with the outside world. Bad data gets blocked automatically with zero `if` statements. Use `response_model` to control what goes out so you never accidentally leak internal fields. One import. Full input/output safety.
