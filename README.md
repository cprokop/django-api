# django-api

Project: mysite
App: Store
App: Warehouse

These are accessed via:

localhost.com/store
localhost.com/warehouse


The top navigation allows for easy switching between the two, but they are indeed separate applications that only talk via their REST API. As well, there are no shared libraries, so there's some amount of redundant code.

In mysite/settings.py are the two data base configurations.  Everything except the 'Warehouse' application should be using 'default'.  'Warehouse' should use 'DB2'.   When I ran the migrations, all the tables seemed to create in both data bases, but I've confirmed that everything is reading/writing where it should.  I didn't check in any of the migration files, so you'll need to make them and migrate each DB.  As well collectstatic.

I installed 'requests' to simplfy some of the API calls.

I know this is a sensitive issue in Python, but I used tabs.  20 years of Perl programming, it'll take a bit for me to switch out of that habit.  Don't fry me.


Other settings:

Warehouse/routers.py
This has the separate Data Base router for the Warehouse app.

mysite/settings.py:

ALLOWED_HOSTS = [ 'HOSTS' ]
DATABASES = {}


Update the www host for the API calls bewtween the apps:

Store/views.py
WAREHOUSE_URL = "http://HOST/warehouse/api/"

Warehouse/views.py
STORE_URL = "http://HOST/store/api/"







