from fastapi import APIRouter, HTTPException, Depends
from typing import List

from ..schemas import User_in, User_out, Update_user
from ..crud import get_user, get_users, create_user, del_user, update_user, check_user_name, check_user_email
from ..auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=List[User_out])
async def read_users(current_user: User_out = Depends(get_current_user)):
    users = get_users()
    if current_user.role == 'admin':
        return users
    raise HTTPException(status_code=403, detail="Not authorized")

@router.get("/{user_id}", response_model=User_out)
async def read_user(user_id: str, current_user: User_out = Depends(get_current_user)):
    user = get_user(user_id=user_id)
    if user:
        if user['_id'] == current_user.id or current_user.role == 'admin':
            return user
        raise HTTPException(status_code=403, detail="Not authorized")
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/create", response_model=User_out, status_code=201)
async def add_user(user: User_in):
    user_dict = user.dict()
    user_name = user_dict['user_name']
    user_email = user_dict['email']
    name_check = check_user_name(user_name)
    email_check = check_user_email(user_email)
    if (name_check or email_check):
        raise HTTPException(status_code=409, detail="Cannot create, already a user with that name or email")
    return create_user(user=user)

@router.delete("/delete/{user_id}")
async def delete_user(user_id: str, current_user: User_out = Depends(get_current_user)):
    user = get_user(user_id=user_id)
    if user:
        if user['_id'] == current_user.id or current_user.role == 'admin':
            del_user(user_id=user_id)
            return
        raise HTTPException(status_code=403, detail="Not authorized")    
    raise HTTPException(status_code=404, detail="User not found")

@router.patch("/update/{user_id}", response_model=User_out)
async def update_users(user_id: str, user: Update_user, current_user: User_out = Depends(get_current_user)):
    user_is = get_user(user_id=user_id)
    if user_is:
        if user_is['_id'] == current_user.id or current_user.role == 'admin':
            update_dict = user.dict(exclude_unset=True)
            return update_user(user_id=user_id, update_dict=update_dict)
        raise HTTPException(status_code=403, detail="Not authorized")
    raise HTTPException(status_code=404, detail="User not found")