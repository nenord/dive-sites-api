from fastapi import APIRouter, HTTPException
from slugify import slugify
from typing import List

from ..schemas import Site, Site_in, Update_site
from ..crud import get_sites, get_site, create_site, del_site, update_site

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
async def add_site(site: Site_in):
    site_dict = site.dict()
    slug = slugify(site_dict.get('name'))
    check_site = get_site(site_id=slug)
    if check_site:
       raise HTTPException(status_code=409, detail="Cannot create, already a site with that name")
    return create_site(site=site, slug=slug)

@router.delete("/delete/{site_id}")
async def delete_site(site_id: str):
    check_site = get_site(site_id=site_id)
    if check_site:
        del_site(site_id=site_id)
        return
    raise HTTPException(status_code=404, detail="Site not found")

@router.patch("/update/{site_id}", response_model=Site)
async def update_site(site_id: str, site: Update_site):
    check_site = get_site(site_id=site_id)
    if check_site:
        update_dict = site.dict(exclude_unset=True)
        return update_site(site_id=site_id, update_dict=update_dict)
    raise HTTPException(status_code=404, detail="Site not found")