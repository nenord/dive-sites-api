# dive-sites-api
API for a crowdsourced dive sites app

Built using fastAPI couchDB

A **work in progress** example: http://api.nenoapps.tk

Deployed via Dokku running on Google Cloud VM.

## Roadmap

Reset password endpoint - via email

Support for images using CouchDB attachments

## Run the app locally
Run a CouchDB docker image with:

```docker run -d --name my-couchdb -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=password -p 5984:5984 couchdb:latest```

This will run a CouchDB database in a Docker container.

Setup the following environment variables:
1.	TEST=```<any string>``` (it just needs to exist and be some non-null/non-false value; used for the environment to know it is on dev and pick up Docker container database)
2.	USER=admin
3.	PASSWORD=password
4.	EXPIRE_TOKEN=30 (this is just example; it can be longer or less but needs to be an integer; token expiration time in minutes)
5.	COUCHDB_URL=http://127.0.0.1:5984
6.	SECRET_KEY=```<some complicated hard to guess string>``` (used for encoding jwt tokens)

Setup a venv virtual environment and then enter the virtual environment.
Install requirements: 

```pip install requirements.txt```

Run the app from the root folder with uvicorn: 

```uvicorn app.main:app```

## Run the app on Dokku

Assumption: You have a Dokku system running on a VM by following this guide: https://dokku.com/docs/getting-started/installation/

Create the app using this guide (do not create a Postgres database or deploy the app yet, just create it): https://dokku.com/docs/deployment/application-deployment/#create-the-app

### Set up a database

Install a CouchDB plugin: 

```sudo dokku plugin:install https://github.com/dokku/dokku-couchdb.git couchdb```

Create a CouchDB databases (call them ‘sites’ and 'users'):

```dokku couchdb:create sites```

```dokku couchdb:create users```

Link the sites database with your app:

```dokku couchdb:link sites <your app>  --alias COUCHDB_SITES```

```dokku couchdb:link users <your app>  --alias COUCHDB_USERS```

This will create an environment variable in your app that will look something like this:

```COUCHDB_SITES_URL=http://sites:<generated-complex-password>@dokku-couchdb-sites:5984/sites```

```COUCHDB_USERS_URL=http://users:<generated-complex-password>@dokku-couchdb-sites:5984/users```

Now your CouchDB instance has databases called ‘sites’ and ‘users’.

### Deploy the app

Before deploying the app, add two environment variables:

```dokku config:set <your app> EXPIRE_TOKEN=30 SECRET_KEY =<some complicated hard to guess string>```

Note: EXPIRE_TOKEN variable can be more or less, as long as it is an int (it controls jwt token expiry)

Now you can deploy the app using: https://dokku.com/docs/deployment/application-deployment/#deploy-the-app 


#### After cuccessful app deployment, your app should now be ready to use.



