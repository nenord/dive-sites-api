from fastapi import APIRouter, HTTPException, Depends
from slugify import slugify
from typing import List

from ..schemas import Site, Site_in, Update_site, User_out
from ..crud import get_sites, get_site, create_site, del_site, update_site
from ..auth import get_current_user

router = APIRouter(
    prefix="/sites",
    tags=["sites"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=List[Site])
async def read_sites():
    sites = get_sites()
    return sites

@router.get("/{site_id}", response_model=Site)
async def read_site(site_id: str):
    site = get_site(site_id=site_id)
    if site:
        return site
    raise HTTPException(status_code=404, detail="Site not found")

@router.post("/create", response_model=Site, status_code=201)
async def add_site(site: Site_in, current_user: User_out = Depends(get_current_user)):
    site_dict = site.dict()
    slug = slugify(site_dict.get('name'))
    check_site = get_site(site_id=slug)
    if check_site:
       raise HTTPException(status_code=409, detail="Cannot create, already a site with that name")
    return create_site(site=site, slug=slug, owner=current_user.id)

@router.delete("/delete/{site_id}")
async def delete_site(site_id: str, current_user: User_out = Depends(get_current_user)):
    site = get_site(site_id=site_id)
    if site:
        if current_user.role == 'admin':
            del_site(site_id=site_id)
            return
        raise HTTPException(status_code=403, detail="Not authorized")
    raise HTTPException(status_code=404, detail="Site not found")

@router.patch("/update/{site_id}", response_model=Site)
async def update_sites(site_id: str, site: Update_site, current_user: User_out = Depends(get_current_user)):
    site_is = get_site(site_id=site_id)
    if site_is:
        if site_is['owner_id'] == current_user.id or current_user.role == 'admin':
            update_dict = site.dict(exclude_unset=True)
            return update_site(site_id=site_id, update_dict=update_dict)
        raise HTTPException(status_code=403, detail="Not authorized")
    raise HTTPException(status_code=404, detail="Site not found")