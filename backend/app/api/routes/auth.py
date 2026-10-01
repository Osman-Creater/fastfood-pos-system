from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.deps import get_current_user
from app.auth.security import create_access_token, verify_password
from app.seed_data import get_demo_user

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    demo_user = get_demo_user(form_data.username)
    if demo_user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    fallback_hash = "$2b$12$QeYQbQ8vB5qQ2xjv6k63X.U35L5fE0Y3d2kQ5r3R0w0A4HX5T7wqxK"
    if not verify_password(form_data.password, fallback_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token(demo_user["username"])
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def me(current_user=Depends(get_current_user)):
    return {"user": current_user}
