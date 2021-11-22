import os
from cloudant import couchdb
from .schemas import Site_in, User_in, User_out, User_inDB
from .helpers import parse_url, get_password_hash
from datetime import datetime

if os.environ.get('TEST'):
    USER_S = os.environ.get('USER')
    PASSWORD_S = os.environ.get('PASSWORD')
    COUCHDB_URL_S = os.environ.get('COUCHDB_URL')
    USER_U = USER_S
    PASSWORD_U = PASSWORD_S
    COUCHDB_URL_U = COUCHDB_URL_S
else:
    url_str_s = parse_url(os.environ.get('COUCHDB_SITES_URL'))
    USER_S = url_str_s[0]
    PASSWORD_S = url_str_s[1]
    COUCHDB_URL_S = url_str_s[2]
    url_str_u = parse_url(os.environ.get('COUCHDB_USERS_URL'))
    USER_U = url_str_u[0]
    PASSWORD_U = url_str_u[1]
    COUCHDB_URL_U = url_str_u[2]

# SITES - helper functions

def get_sites(skip: int = 0, limit: int = 100):
    with couchdb(USER_S, PASSWORD_S, url=COUCHDB_URL_S) as client:
        sitesdb = client['sites']
        sites = [site for site in sitesdb]
    return sites

def get_site(site_id: str):
    with couchdb(USER_S, PASSWORD_S, url=COUCHDB_URL_S) as client:
        sites = client['sites']
        if (site_id in sites):
            return sites[site_id]

def create_site(site: Site_in, slug: str, owner: str):
    site_dict = site.dict()
    site_dict.update([('_id', slug), ('owner_id', owner), 
        ('created_on_utc', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'))])
    with couchdb(USER_S, PASSWORD_S, url=COUCHDB_URL_S) as client:
        sites = client['sites']
        new_site = sites.create_document(site_dict)
        return new_site

def del_site(site_id: str):
    with couchdb(USER_S, PASSWORD_S, url=COUCHDB_URL_S) as client:
        sites = client['sites']
        site = sites[site_id]
        site.delete()

def update_site(site_id: str, update_dict: dict):
    with couchdb(USER_S, PASSWORD_S, url=COUCHDB_URL_S) as client:
        sites = client['sites']
        site = sites[site_id]
        for key, value in update_dict.items():
            site[key] = value
            site.save()
        return site

# USERS - helper functions

def get_users(skip: int = 0, limit: int = 100):
    with couchdb(USER_U, PASSWORD_U, url=COUCHDB_URL_U) as client:
        usersdb = client['users']
        users = [user for user in usersdb]
    return users

def get_user(user_id: str):
    with couchdb(USER_U, PASSWORD_U, url=COUCHDB_URL_U) as client:
        users = client['users']
        if (user_id in users):
            return users[user_id]

def create_user(user: User_in):
    user_dict = user.dict()
    hash_password = get_password_hash(user_dict['password'])
    user_dict.pop('password')
    user_dict.update([
        ('password_hash', hash_password),
        ('registered_on_utc', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')),
        ('role', 'standard')
    ])
    with couchdb(USER_U, PASSWORD_U, url=COUCHDB_URL_U) as client:
        users = client['users']
        new_user = users.create_document(user_dict)
        return new_user

def del_user(user_id: str):
    with couchdb(USER_U, PASSWORD_U, url=COUCHDB_URL_U) as client:
        users = client['users']
        user = users[user_id]
        user.delete()

def update_user(user_id: str, update_dict: dict):
    with couchdb(USER_U, PASSWORD_U, url=COUCHDB_URL_U) as client:
        users = client['users']
        user = users[user_id]
        for key, value in update_dict.items():
            user[key] = value
            user.save()
        return user

def check_user_name(user_name: str):
    with couchdb(USER_U, PASSWORD_U, url=COUCHDB_URL_U) as client:
        users = client['users']
        selector = {'user_name': {'$eq': user_name}}
        docs = users.get_query_result(selector)
        if len(docs[0]):
            return User_out(**docs[0][0])

def check_user_email(user_email: str):
    with couchdb(USER_U, PASSWORD_U, url=COUCHDB_URL_U) as client:
        users = client['users']
        selector = {'email': {'$eq': user_email}}
        docs = users.get_query_result(selector)
        if len(docs[0]):
            return User_inDB(**docs[0][0])