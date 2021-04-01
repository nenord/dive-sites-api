from fastapi import APIRouter, HTTPException

from ..schemas import User, User_in, User_out, User_inDB
from ..crud import get_user, create_user, del_user

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
    return create_user(user=user)

@router.delete("/delete/{user_id}")
async def delete_user(user_id: str):
    check_user = get_user(user_id=user_id)
    if check_user:
        del_user(user_id=user_id)
        return
    raise HTTPException(status_code=404, detail="User not found")
"""
@router.patch("/update/{site_id}", response_model=Site)
async def update_site(site_id: str, site: Update_site):
    check_site = get_site(site_id=site_id)
    if check_site:
        update_dict = site.dict(exclude_unset=True)
        return update_site(site_id=site_id, update_dict=update_dict)
    raise HTTPException(status_code=404, detail="Site not found")
"""