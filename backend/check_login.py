import json
import urllib.request
import urllib.error
import getpass

url = "http://127.0.0.1:5000/api/login"

email = input("Enter admin email: ")
password = getpass.getpass("Enter admin password: ")

data = json.dumps({
    "email": email,
    "password": password
}).encode("utf-8")

req = urllib.request.Request(
    url,
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=10) as response:
        print("HTTP Status:", response.status)
        print("Response:", response.read().decode())

except urllib.error.HTTPError as e:
    print("HTTP Status:", e.code)
    print("Response:", e.read().decode())

except Exception as e:
    print("Connection Error:", str(e))
