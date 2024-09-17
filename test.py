import requests

url = "https://api.oceansedge.frostboltinteractive.com/Endpoints/getServerList.py"
response = requests.get(url)

if response.status_code == 200:
    print("Success!")
    print(response.json())
else:
    print("Failed to retrieve data:", response.status_code)
