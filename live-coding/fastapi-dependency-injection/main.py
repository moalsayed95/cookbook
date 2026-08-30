from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, status

app = FastAPI()

DEMO_API_KEY = "sayeddev-secret"


# Broken: the same API-key check is copied into every endpoint.
@app.get("/reports-bad")
async def get_reports_bad(
    x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
):
    if x_api_key != DEMO_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key",
        )

    return {"reports": ["sales", "traffic"]}


@app.get("/settings-bad")
async def get_settings_bad(
    x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
):
    if x_api_key != DEMO_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key",
        )

    return {"theme": "light", "notifications": True}


# Fixed: FastAPI runs this once before each endpoint that depends on it.
def require_api_key(
    x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
) -> str:
    if x_api_key != DEMO_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key",
        )

    return "cookbook-client"


@app.get("/reports")
async def get_reports(
    current_client: Annotated[str, Depends(require_api_key)],
):
    return {
        "client": current_client,
        "reports": ["sales", "traffic"],
    }


@app.get("/settings")
async def get_settings(
    current_client: Annotated[str, Depends(require_api_key)],
):
    return {
        "client": current_client,
        "theme": "light",
        "notifications": True,
    }