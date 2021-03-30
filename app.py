from fastapi import FastAPI, Depends, HTTPException
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from slugify import slugify

from crud import get_sites, get_site, create_site, del_site, update_site
from schemas import Site, Site_in, Update_site, User, User_in, User_inDB

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to my API, please go to /docs to see details."}

@app.get("/sites", response_model=List[Site])
async def read_items():
    sites = get_sites()
    return sites

@app.get("/sites/{site_id}", response_model=Site)
async def read_site(site_id: str):
    site = get_site(site_id=site_id)
    if site:
        return site
    raise HTTPException(status_code=404, detail="Site not found")

@app.post("/create_site", response_model=Site, status_code=201)
async def add_item(site: Site_in):
    site_dict = site.dict()
    slug = slugify(site_dict.get('name'))
    check_site = get_site(site_id=slug)
    if check_site:
       raise HTTPException(status_code=409, detail="Cannot create, already a site with that name")
    return create_site(site=site, slug=slug)

@app.delete("/delete_site/{site_id}")
async def read_site(site_id: str):
    check_site = get_site(site_id=site_id)
    if check_site:
        del_site(site_id=site_id)
        return
    raise HTTPException(status_code=404, detail="Site not found")

@app.patch("/update_site/{site_id}", response_model=Site)
async def read_site(site_id: str, site: Update_site):
    check_site = get_site(site_id=site_id)
    if check_site:
        update_dict = site.dict(exclude_unset=True)
        return update_site(site_id=site_id, update_dict=update_dict)
    raise HTTPException(status_code=404, detail="Site not found")
