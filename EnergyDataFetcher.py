from Energy.Factory import CreateApp
import configparser
import os 
# flask -A Energy run --debug


config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join("Energy/config")))

if __name__ == "__main__":
	app = CreateApp()
	app.config['DEBUG'] = True
	app.config['MONGO_URI'] = config['PROD']['DB_URI']
	
	app.run()