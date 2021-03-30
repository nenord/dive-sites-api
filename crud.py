from cloudant import couchdb
from schemas import Site_in, Site
import os

USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD')
COUCHDB_URL = os.environ.get('COUCHDB_URL')

def get_sites(skip: int = 0, limit: int = 100):
    with couchdb(USER, PASSWORD, url=COUCHDB_URL) as client:
        sitesdb = client['sites']
        sites = [site for site in sitesdb]
    return sites

def get_site(site_id: str):
    with couchdb(USER, PASSWORD, url=COUCHDB_URL) as client:
        sites = client['sites']
        if (site_id in sites):
            return sites[site_id]

def create_site(site: Site_in, slug: str):
    site_dict = site.dict()
    site_dict.update({'_id': slug})
    with couchdb(USER, PASSWORD, url=COUCHDB_URL) as client:
        sites = client['sites']
        new_site = sites.create_document(site_dict)
        return new_site

def del_site(site_id: str):
    with couchdb(USER, PASSWORD, url=COUCHDB_URL) as client:
        sites = client['sites']
        site = sites[site_id]
        site.delete()

def update_site(site_id: str, update_dict: dict):
    with couchdb(USER, PASSWORD, url=COUCHDB_URL) as client:
        sites = client['sites']
        site = sites[site_id]
        for key, value in update_dict.items():
            site[key] = value
            site.save()
        return site
