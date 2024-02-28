import requests


create_user = "createuser"
get_devices = "getdevices"
add_cloud_credentials = "addcloudcredentials"
login = "login"
url = "http://zainkhan.ddns.net:5000/api/v1/energy"
data = {"email":"a@z", "password":"p", "name":"a"}
token = "REDACTED_ROTATE_ME"

secret = "REDACTED_ROTATE_ME"
cloud_credentials = {"token" : "REDACTED_ROTATE_ME", "secret" : "REDACTED_ROTATE_ME"}


def GetCompleteURL(sub_url):
	final_url = url + "/" + sub_url
	return final_url


print(f"Creating User: {data}")
final_url = GetCompleteURL(create_user)
res = requests.post(final_url, json=data)
print(res.text)

print(f"Logging User: {data}")
final_url = GetCompleteURL(login)
res = requests.post(final_url, json=data)
print(res.json())
if res.status_code == 200:
	auth_header = {"Authorization" : f"Bearer {res.json()['access_token']}"}
else:
	auth_header = {}

print(auth_header)

if len(auth_header) == 0:
	print("Auth Header empty, exiting.")
	exit()

print(f"Adding Cloud Credentials")
final_url = GetCompleteURL(add_cloud_credentials)
res = requests.post(final_url, json=cloud_credentials, headers = auth_header)
print(res.text)