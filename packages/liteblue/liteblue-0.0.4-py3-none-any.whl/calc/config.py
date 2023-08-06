""" Configuration settings for calc """
import os
from pkg_resources import resource_filename
from liteblue import config

class Config(config.Config):
    """ overide of default config """
    
    name = "calc"
    procedures = "calc.procedures"
    
    tornado_debug = True
    static_path = resource_filename('liteblue.apps', 'static')

    db_url = os.getenv('DB_URL', 'sqlite:///calc.db')
    alembic_script_location = resource_filename('calc', 'scripts')