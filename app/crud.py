import os
from cloudant import couchdb
from .schemas import Site_in, User_in
from passlib.context import CryptContext
from .parse_db import parse_url

if os.environ.get('TEST'):
    USER = os.environ.get('USER')
    PASSWORD = os.environ.get('PASSWORD')
    COUCHDB_URL = os.environ.get('COUCHDB_URL')
else:
    url_str = os.environ.get('COUCHDB_URL')
    USER = url_str[0]
    PASSWORD = url_str[1]
    COUCHDB_URL = url_str[2]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SITES - helper functions

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

# USERS - helper functions

def get_user(user_id: str):
    with couchdb(USER, PASSWORD, url=COUCHDB_URL) as client:
        users = client['users']
        if (user_id in users):
            return users[user_id]

def create_user(user: User_in):
    user_dict = user.dict()
    hash_password = pwd_context.hash(user_dict['password'])
    user_dict['password'] = hash_password
    user_dict.update({'active': True})
    with couchdb(USER, PASSWORD, url=COUCHDB_URL) as client:
        users = client['users']
        new_user = users.create_document(user_dict)
        return new_user

def del_user(user_id: str):
    with couchdb(USER, PASSWORD, url=COUCHDB_URL) as client:
        users = client['users']
        user = users[user_id]
        user.delete()

def update_user(user_id: str, update_dict: dict):
    with couchdb(USER, PASSWORD, url=COUCHDB_URL) as client:
        users = client['users']
        user = users[user_id]
        for key, value in update_dict.items():
            user[key] = value
            user.save()
        return user

def check_user_name(user_name: str):
    with couchdb(USER, PASSWORD, url=COUCHDB_URL) as client:
        users = client['users']
        selector = {'user_name': {'$eq': user_name}}
        docs = users.get_query_result(selector)
        if len(docs[0]):
            return docs[0][0]

def check_user_email(user_email: str):
    with couchdb(USER, PASSWORD, url=COUCHDB_URL) as client:
        users = client['users']
        selector = {'email': {'$eq': user_email}}
        docs = users.get_query_result(selector)
        if len(docs[0]):
            return docs[0][0]

