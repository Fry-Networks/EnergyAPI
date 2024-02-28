import cloudinary

cloudinary.config(
cloud_name = "dpynlgyfi",
api_key = "591242394252752",
api_secret = "REDACTED_ROTATE_ME",
# api_proxy = config["api_proxy"]
)

import os
import datetime
import cloudinary.uploader
import cloudinary.api
import requests


class RemoteDataHandler:
	def __init__(self):
		pass

	def UploadToCloud(self, filepath, publid_id, resource_type = "image"):
		# print("publid_id", publid_id)
		res = cloudinary.uploader.upload(filepath,
										publid_id = publid_id, 
										folder = "energy_data_graphs",
										overwrite = True
										)

		res = cloudinary.uploader.rename(
			res["public_id"],
			f"energy_data_graphs/{publid_id}",
			overwrite = True,
			type="upload",
			resource_type="image")

		print(res["url"])

		return res

	def DeleteFilesNow(self, publicIDs):
		for obj in publicIDs:
			print(f"Deleting {obj[0]}")
			cloudinary.uploader.destroy(obj[0], resource_type = obj[1])

	def DownloadData(self, url, root_dir):
		local_filepath = os.path.join(root_dir, url.split("/")[-1])

		with requests.get(url, stream=True) as r:
			r.raise_for_status()
			with open(local_filepath, 'wb') as f:
				for chunk in r.iter_content(chunk_size=8192): 
					f.write(chunk)	

		return local_filepath
