from Energy.Factory import CreateApp
import configparser
import os 

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join("Energy/config")))

app = CreateApp()
app.config['DEBUG'] = True
app.config['MONGO_URI'] = config['PROD']['DB_URI']

celery_app = app.extensions["celery"]
