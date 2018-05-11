# django-api

Project: mysite
App: Store
App: Warehouse

These are accessed via:

localhost.com/store
localhost.com/warehouse


The top navigation allows for easy switching between the two, but they are indeed separate applications that only talk via their REST API. As well, there are no shared libraries, so a bit of redundant code.

In mysite/settings.py are the two data base configurations.  Everything except the 'Warehouse' application should be using 'default'.  'Warehouse' should use 'DB2'.   When I ran the migrations, all the tables seemed to create in both data bases, although it seems to be reading and writing appropriately between them.


Make migrations, collectstatic.  I installed 'requests' to simplfy some of the API calls.


mysite/settings.py:

ALLOWED_HOSTS = [ 'HOSTS' ]
DATABASES = {}





