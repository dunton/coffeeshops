#!/usr/bin/python
import sys
import logging
import os.path
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, 'var/www/coffeeshops/catalog/')
from database_setup import create_database
from database_populator import populate_database
from views import app as application

application.config['DATABASE_URL'] = 'sqlite:////var/www/coffeeshops/catalog/coffeeshopmenu.db'

# Create database and populate it, if not already done so.
if os.path.isfile('var/www/coffeeshops/catalog/coffeeshopmenu.db') is False:
    create_database(application.config['DATABASE_URL'])
    populate_database()
