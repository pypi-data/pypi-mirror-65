from requests import post, get
import json
from zipfile import ZipFile
import glob

def deploy(path, domain, personal_access_token, temp_zip_path="/tmp/site.zip"):
	with ZipFile(temp_zip_path, "w") as z:
		for file in glob.glob(path):
			z.write(file)
	with open(temp_zip_path, "rb") as f:
		response = post(f"https://api.netlify.com/api/v1/sites/{domain}/deploys?access_token={token}",
		headers={
			"Content-Type":"application/zip"
		},
		data=f)
	return response.json()