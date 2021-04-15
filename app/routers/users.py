from fastapi import APIRouter, HTTPException

from ..schemas import User, User_in, User_out, Update_user
from ..crud import get_user, create_user, del_user, update_user, check_user_name, check_user_email

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

@router.get("/{user_id}", response_model=User_out)
async def read_user(user_id: str):
    user = get_user(user_id=user_id)
    if user:
        return user
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
async def delete_user(user_id: str):
    check_user = get_user(user_id=user_id)
    if check_user:
        del_user(user_id=user_id)
        return
    raise HTTPException(status_code=404, detail="User not found")

@router.patch("/update/{user_id}", response_model=User_out)
async def update_users(user_id: str, user: Update_user):
    check_user = get_user(user_id=user_id)
    if check_user:
        update_dict = user.dict(exclude_unset=True)
        return update_user(user_id=user_id, update_dict=update_dict)
    raise HTTPException(status_code=404, detail="User not found")