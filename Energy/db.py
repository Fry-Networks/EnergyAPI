import bson

from flask import current_app, g
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId
from werkzeug.local import LocalProxy
from Energy.RemoteDataHandler import RemoteDataHandler




def GetDB():
	db = getattr(g, "_database", None)

	if db is None:

		db = g._database = PyMongo(current_app).db
	   
	return db


db = LocalProxy(GetDB)


def Hello():
	print("DB HELLO")
	print(db)

def GetAllEmails():
	all_emails = []
	for document in db.users.find():
		all_emails.append(document["email"])

	return all_emails

# GetDataFor and GetUser are doing the same thing, remove one of them
def GetDataFor(email):
	data = db.users.find_one({"email": email})
	if data is not None:
		return data

	return data

def GetUser(email):
	data = db.users.find_one({"email": email})
	if data is not None:
		return data
	return None

def GetUsageDataFor(email):
	data = db.device_info.find_one({"email": email})
	if data is not None:
		return data

def AddUser(email, name, password_hash):
	data = {"email" : email, "name" : name, "password" : password_hash, "cloud_credentials" : None, "devices": []}
	db.users.insert_one(data)

	data = {"email" : email, "devices" : {}}
	db.device_info.insert_one(data)

def UserExists(email):
	data = db.users.find_one({"email": email})
	if data is not None:
		return True
	return False


def AddUserCloudCredentials(email, credentials):
	data = db.users.find_one({"email": email})
	if data is not None:
		if data["cloud_credentials"] is None:
			data["cloud_credentials"] = credentials
			f = { '_id': data["_id"]}
			new_values = { "$set": { "cloud_credentials" : credentials} }
			db.users.update_one(f, new_values)
			return True
		
		else:
			return False

	return False


def AddDevices(email, devices):
	data = db.users.find_one({"email": email})
	if data is not None:
		f = { '_id': data["_id"]}
		new_values = { "$set": { "devices" : devices} }
		db.users.update_one(f, new_values)
	
	device_data = {}
	data = db.device_info.find_one({"email": email})


	print(data["devices"].keys())
	if data is not None:
		for device in devices:
			if device["deviceId"] in data["devices"]:
				device_data[device["deviceId"]] = data["devices"][device["deviceId"]]
				continue


			device_data[device["deviceId"]] = {
												"deviceName" : device["deviceName"], 
												"deviceType" : device["deviceType"],
												"data" : {
															"date" : [],
															"voltage" : [],
															"current" : [],
															"energy" : [],
															"upTime" : [],
															"power" : []

														 },
												 "totalPower" : 0,
												 "totalEnergy" : 0,
												 "totalCost" : 0
											  }

		for dev_ID in data["devices"].keys():
			if dev_ID not in device_data:
				device_data[dev_ID] = data["devices"][dev_ID]


		f = { '_id': data["_id"]}
		new_values = { "$set": { "devices" : device_data} }
		db.device_info.update_one(f, new_values)
		print(device_data)




def AddDeviceData(email, device_ID, date, voltage, current, upTime, power):
	# device_data = {"email" : email, 
	# 				"devices" : {
	# 								"<deviceID>" : { 
	# 												"deviceName" : "<deviceName>", 
	# 												"deviceType" : "<deviceType>", 
	# 												"data" : {
	# 															"date" : [],
	# 															"voltage" : [],
	# 															"current" : [],
	# 															"power" : []
	# 														  }
	# 												"totalPower" : 0,
	# 												"totalEnergy" : 0
	# 											 }
	# 							}
	# 			  }

	data = db.device_info.find_one({"email": email})
	if data is not None:
		if device_ID in data['devices']:
			data["devices"][device_ID]["data"]["date"].append(date)
			data["devices"][device_ID]["data"]["voltage"].append(voltage)
			data["devices"][device_ID]["data"]["current"].append(current)
			data["devices"][device_ID]["data"]["energy"].append(energy)
			data["devices"][device_ID]["data"]["upTime"].append(upTime)
			data["devices"][device_ID]["data"]["power"].append(power)

			data["devices"][device_ID]['totalEnergy'] = power * (upTime / 60)
			data["devices"][device_ID]['totalCost'] = data["devices"][device_ID]['totalEnergy']

			f = { '_id': data["_id"]}
			new_values = { "$set": { "devices" : data["devices"]} }
			db.device_info.update_one(f, new_values)