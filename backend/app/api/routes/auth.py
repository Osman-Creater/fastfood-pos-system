from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.security import create_access_token, verify_password
from app.auth.deps import get_current_user

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Replace with DB lookup in production
    demo_user = {
        "username": form_data.username,
        "password_hash": "$2b$12$QeYQbQ8vB5qQ2xjv6k63X.U35L5fE0Y3d2kQ5r3R0w0A4HX5T7wqxK",
        "roles": ["cashier", "shift_supervisor"],
        "location_id": "loc-001",
    }

    if form_data.username != demo_user["username"]:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not verify_password(form_data.password, demo_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token(demo_user["username"])
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def me(current_user=Depends(get_current_user)):
    return {"user": current_user}
