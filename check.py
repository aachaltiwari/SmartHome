import requests

url = "http://127.0.0.1:8000/auth/users/me/"
headers = {"Authorization": "JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA2ODAyODk5LCJpYXQiOjE3MDY3MTY0OTksImp0aSI6IjhlY2Q4YjIxOGVhODRkMjE4MjA0MmU5MzFmYjJhZmYyIiwidXNlcl9pZCI6NX0.gqtOZeBU9H3dgL87pzLneTo3mBFB0cRktUGWF99dXIM"
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    user_data = response.json()
    print(user_data)
else:
    print(f"Error: {response.status_code}, {response.text}")