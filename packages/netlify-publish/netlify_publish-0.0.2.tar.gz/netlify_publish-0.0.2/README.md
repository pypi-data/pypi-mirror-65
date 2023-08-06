# Netlify deploy
#### This is used for publishing static files
Publish static files easily using the `deploy()` function

```python

from netlify_publish.publish import deploy
deploy("/tmp/*.html", "domain.netlify.com", "<personal_access_token>", 
		temp_zip_path="/temp/temp.zip")

```

- personal_access_token: you can get it from [here](https://app.netlify.com/user/applications)
- temp_zip_path: is optional