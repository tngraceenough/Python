#pip install requests


import requests 
response = requests.get("https://api.publicapis.org/entries")
response.status_code


import requests 
response = requests.get("https://catfact.ninja/fact")
response.status_code


import requests 
response = requests.get("https://randomuser.me/api")
response.status_code
