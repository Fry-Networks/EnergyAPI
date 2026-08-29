from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

from flask import Blueprint, request, jsonify
from Energy.db import Hello, AddUser, AddUserCloudCredentials, UserExists, GetUser, AddDevices, GetUsageDataFor
from Energy.SwitchBotCloudInterface import GetDevicesFromSwitchBot
from flask import current_app


energy_api_v1 = Blueprint('energy_api_v1', 'energy_api_v1', url_prefix='/api/v1/energy')


@energy_api_v1.route('/login', methods=['POST'])
def Login():
	data = request.get_json()
	email = data["email"]
	password = data["password"]

	user_data = GetUser(email)
	if user_data is None :
		return {"msg" : "Bad username or password"}, 401

	if not check_password_hash(user_data["password"], password):
		return {"msg": "Bad username or password"}, 401

	access_token = create_access_token(identity=email)
	usage_date = GetUsageDataFor(email)

	if usage_date is None:
		return {"access_token" : access_token, "name" : user_data["name"], "device_data" : {}, "cloud_credentials_exist" : user_data["cloud_credentials"] is not None}, 200
	
	return {"access_token" : access_token, "name" : user_data["name"], "device_data" : usage_date["devices"], "cloud_credentials_exist" : user_data["cloud_credentials"] is not None}, 200


@energy_api_v1.route('/createuser', methods=['POST'])
def CreateUser():
	data = request.get_json()

	email = data['email']
	name = data['name']
	password = generate_password_hash(data['password'])

	if not UserExists(email):
		AddUser(email, name, password)
		return {"msg" : "User Created"}, 200
	else:
		return {"msg" : "User not created, User already exists"}, 401


@energy_api_v1.route('/refreshdevices', methods=['POST', 'GET'])
@jwt_required()
def RefreshDevices():
	current_user_email = get_jwt_identity()
	user_data = GetUser(current_user_email)

	if user_data["cloud_credentials"] is not None:
		all_devices = GetDevicesFromSwitchBot(user_data["cloud_credentials"]["token"], user_data["cloud_credentials"]["secret"])
		if len(all_devices) > 0:
			AddDevices(current_user_email, all_devices)
			return {"msg" : f"Num new devices added: {len(all_devices)}"}, 200

			return {"msg" : "Credentials couldn't be added"}, 401



@energy_api_v1.route("/getuserdata", methods = ["GET"])
@jwt_required()
def GetUserData():
	current_user_email = get_jwt_identity()
	user_data = GetUser(current_user_email)

	if user_data is None :
		return {"msg" : "User does not exists"}, 401

	usage_date = GetUsageDataFor(current_user_email)
	if usage_date is None :
		data = {"email" : current_user_email, "name" : user_data["name"], "device_data" : {}}

	data = {"email" : current_user_email, "name" : user_data["name"], "device_data" : usage_date["devices"], "cloud_credentials_exist" : user_data["cloud_credentials"] is not None}
	return data, 200



@energy_api_v1.route('/getdevices', methods=['POST', "GET"])
@jwt_required()
def GetDevices():
	current_user_email = get_jwt_identity()
	return {"devices": []}, 200


@energy_api_v1.route('/addcloudcredentials', methods=['POST'])
@jwt_required()
def AddCloudCredentials():
	data = request.get_json()

	token = data['token']
	secret = data['secret']

	current_user_email = get_jwt_identity()

	success = AddUserCloudCredentials(current_user_email, {"token" : token, "secret" : secret})

	if success:
		all_devices = GetDevicesFromSwitchBot(token, secret)
		AddDevices(current_user_email, all_devices)

		return {"msg" : "Added credentials successfully"}, 200

	else:
		return {"msg" : "Credentials couldn't be added"}, 401

@energy_api_v1.route('/getpowerusage', methods=['POST', "GET"])
@jwt_required()
def GetPowerUsageData():
	current_user_email = get_jwt_identity()
	pass