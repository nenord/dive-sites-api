from sqlalchemy.orm import Session

from app.models import Site_db
from app.schemas import Site_in, Site

def get_site(db: Session, site_slug: str):
    return db.query(Site_db).filter(Site_db.slug == site_slug).first()

def get_sites(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Site_db).offset(skip).limit(limit).all()

def create_site(db: Session, site: Site_in, slug: str):
    site_dict = site.dict()
    site_dict.update({"slug": slug})
    db_site = Site_db(**site_dict)
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site