from fastapi import FastAPI, Depends, HTTPException
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse

from .routers import sites, users
from .crud import check_user_email
from .helpers import verify_password
from .auth import create_access_token, get_current_user
from .schemas import User_out, User_inDB

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sites.router,)
app.include_router(users.router)

@app.get("/")
async def root():
    return RedirectResponse("/docs")

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    login_exception = HTTPException(status_code=400, detail="Incorrect username or password")
    user = check_user_email(form_data.username)
    if not user:
        raise login_exception
    if not verify_password(form_data.password, user.password_hash):
       raise login_exception
    access_token = create_access_token( data={"sub": user.id} )
    return {"access_token": access_token, "user_name": user.user_name, "token_type": "bearer"}

@app.get("/whoami")
async def who_am_i(current_user: User_out = Depends(get_current_user)):
    return current_user


