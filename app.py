#import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from slugify import slugify


from crud import get_site, get_sites, create_site, del_site, update_site
from models import Sitedb, Base
from schemas import Site, Site_in, Update_site
from database import SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
async def read_items(db: Session = Depends(get_db)):
    sites = get_sites(db)
    return sites

@app.post("/create_site", status_code=201)
async def add_item(site: Site_in, db: Session = Depends(get_db)):
    site_dict = site.dict()
    slug = slugify(site_dict.get('name'))
    check_site = get_site(db, site_slug=slug)
    if check_site:
        raise HTTPException(status_code=409, detail="Cannot create, already a site with that name")
    return create_site(db, site=site, slug=slug)

@app.get("/sites/{site_slug}")
async def read_site(site_slug: str, db: Session = Depends(get_db)):
    site = get_site(db, site_slug=site_slug)
    if site:
        return site
    raise HTTPException(status_code=404, detail="Site not found")

@app.delete("/delete_site/{site_slug}")
async def read_site(site_slug: str, db: Session = Depends(get_db)):
    check_site = get_site(db, site_slug=site_slug)
    if check_site:
        del_site(db, site_slug=site_slug)
        return
    raise HTTPException(status_code=404, detail="Site not found")

@app.patch("/update_site/{site_slug}")
async def read_site(site_slug: str, site: Update_site, db: Session = Depends(get_db)):
    check_site = get_site(db, site_slug=site_slug)
    if check_site:
        update_dict = site.dict(exclude_unset=True)
        update_site(db, site=check_site, update_dict=update_dict)
        return get_site(db, site_slug=site_slug)
    raise HTTPException(status_code=404, detail="Site not found")
