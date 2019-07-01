from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from CRUD.flask_celery import make_celery
from flask_caching import Cache
import logging

# DEBUG: Detailed information, typically of interest only when diagnosing problems.

# INFO: Confirmation that things are working as expected.

# WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.

# ERROR: Due to a more serious problem, the software has not been able to perform some function.

# CRITICAL: A serious error, indicating that the program itself may be unable to continue running.

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('logs.log')
file_handler.setFormatter(formatter)

# To print the logs onto the console again. 
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Creating the object of flask
app = Flask(__name__)

# Celery Configurations
app.config['CELERY_BROKER_URL']='amqp://localhost//'
app.config['CELERY_RESULT_BACKEND']='db+postgresql://postgres:123456789@localhost/books_store'

# Flask Caching Configurations with redis and at the same time creating the object cache of type Cache
cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 300000,
    'CACHE_KEY_PREFIX': 'fcache',
    'CACHE_REDIS_HOST': 'localhost',
    'CACHE_REDIS_PORT': '6379',
    'CACHE_REDIS_URL': 'redis://localhost:6379'
    })

# Initializing object of celery
celery=make_celery(app)


# Configurations of sqlalchemy. The password and username are set reading this link:
# https://www.google.com/url?q=https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e&sa=D&source=hangouts&ust=1561189264235000&usg=AFQjCNGxknU5amhR090VzgVhonWdmu_zXQ
database_file='postgresql+psycopg2://postgres:123456789@localhost/books_store'
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# Creating the object of Sqlalchemy
db = SQLAlchemy(app)

from CRUD import routes
from CRUD import tasks

