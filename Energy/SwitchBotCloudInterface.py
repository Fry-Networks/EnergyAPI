import json
import time
import hashlib
import hmac
import base64
import uuid

import requests
import random


base_url = 'https://api.switch-bot.com/v1.1/'

def GetAPIHeader(token, secret, t):
	apiHeader = {}
	# token = "REDACTED_ROTATE_ME"
	# secret = "REDACTED_ROTATE_ME"
	nonce = uuid.uuid4()
	# t = int(round(time.time() * 1000))
	string_to_sign = '{}{}{}'.format(token, t, nonce)

	string_to_sign = bytes(string_to_sign, 'utf-8')
	secret = bytes(secret, 'utf-8')

	sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
	print ('Authorization: {}'.format(token))
	print ('t: {}'.format(t))
	print ('sign: {}'.format(str(sign, 'utf-8')))
	print ('nonce: {}'.format(nonce))

	#Build api header JSON
	apiHeader['Authorization']=token
	apiHeader['Content-Type']='application/json'
	apiHeader['charset']='utf8'
	apiHeader['t']=str(t)
	apiHeader['sign']=str(sign, 'utf-8')
	apiHeader['nonce']=str(nonce)

	return apiHeader

def GetDevicesFromSwitchBot(token, secret, t = None):
	''' 
	{
	'statusCode': 100, 
	'body': {
				'deviceList': [
									{'deviceId': '404CCAA65F92', 
									'deviceName': 'Kitchen Test', 
									'deviceType': 'Plug Mini (US)', 
									'enableCloudService': True, 
									'hubDeviceId': ''}
							  ], 
				'infraredRemoteList': []
			}, 
	'message': 'success'}
	'''

	if token.lower() == "dummy" or secret.lower() == "dummy":
		num_devices = random.randint(1, 7)

		all_devices = []
		for i in range(num_devices):
			all_devices.append({"deviceId" : f"{random.randint(10, 99)}{random.randint(10, 99)}{random.randint(10, 99)}", 
								"deviceName" : f"device{i+1}", 
								"deviceType" : f"Plug"})

		return all_devices



	if t is None:
		t = int(round(time.time() * 1000))

	apiHeader = GetAPIHeader(token, secret, t)

	get_devices_sub_url = "devices"
	url = base_url + get_devices_sub_url
	res = requests.get(url, headers = apiHeader)

	all_devices = []

	if res.status_code == 200:
		for device in res.json()["body"]["deviceList"]:
			all_devices.append({"deviceId" : device["deviceId"], "deviceName" : device["deviceName"], "deviceType" : device["deviceType"]})

	return all_devices

def GetDeviceStatusFromSwitchBot(token, secret, device_ID, t = None):
	'''
	{
	'statusCode': 100, 
	'body': {
				'deviceId': '404CCAA65F92', 
				'deviceType': 'Plug Mini (US)', 
				'hubDeviceId': '404CCAA65F92', 
				'power': 'off', 
				'voltage': 120.8, 
				'weight': 0, 
				'electricityOfDay': 360, 
				'electricCurrent': 0, 
				'version': 'V1.5-1.5'
			}, 
	'message': 'success'}
	'''

	if token.lower() == "dummy" or secret.lower() == "dummy":
		return random.randint(115, 225), random.randint(0, 4), random.randint(50, 100), random.randint(100, 1000)

	if t is None:
		t = int(round(time.time() * 1000))
	apiHeader = GetAPIHeader(token, secret, t)

	get_device_status_sub_url = f"devices/{device_ID}/status"
	url = base_url + get_device_status_sub_url
	res = requests.get(url, headers = apiHeader)


	if res.status_code == 200:
		return res.json()["body"]["voltage"], res.json()["body"]["electricCurrent"], res.json()["body"]["electricityOfDay"], res.json()["body"]["weight"]
