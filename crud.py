from sqlalchemy.orm import Session

from models import Sitedb
from schemas import Site_in, Site

def get_site(db: Session, site_slug: str):
    return db.query(Sitedb).filter(Sitedb.slug == site_slug).first()

def get_sites(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Sitedb).offset(skip).limit(limit).all()

def create_site(db: Session, site: Site_in, slug: str):
    site_dict = site.dict()
    site_dict.update({"slug": slug})
    db_site = Sitedb(**site_dict)
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site

def del_site(db: Session, site_slug: str):
    site_del = db.query(Sitedb).filter(Sitedb.slug == site_slug).first()
    db.delete(site_del)
    db.commit()

def update_site(db: Session, site: Sitedb, update_dict: dict):
    for key, value in update_dict.items():
        setattr(site, key, value) 
    db.commit()
    
