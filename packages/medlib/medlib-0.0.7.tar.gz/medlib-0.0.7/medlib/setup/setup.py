import os
import configparser

def getSetupIni():

    file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'setup.ini')
    parser = configparser.RawConfigParser()
    parser.read( file, encoding='utf-8' )

    version = "0.0.0"
    name = "medlib"
    title = 'medLib'

    try:
        version = parser.get("DEFAULT", 'version')
        name = parser.get("DEFAULT", 'name')
        title = parser.get("DEFAULT", 'title')
    except (configparser.NoSectionError, configparser.NoOptionError):
        pass

    return dict([ 
        ('name', name), 
        ('title', title), 
        ('version', version)
    ])
