import requests
import time

#for temperature hai
def fetch_temp_data():
    url = "https://blynk.cloud/external/api/get?token=nk24hJbhlmcJv9x6n8E49fH-Nx7sMrRb&v6"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

#for humidity hai
def fetch_humidity_data():
    url = "https://blynk.cloud/external/api/get?token=nk24hJbhlmcJv9x6n8E49fH-Nx7sMrRb&v5"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

#for soil_moisture hai
def fetch_soil_moisture_data():
    url = "https://blynk.cloud/external/api/get?token=nk24hJbhlmcJv9x6n8E49fH-Nx7sMrRb&v7"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None
    
#temperature value update in database
def put_temp(temp):
    data = {
    "pk": 12,
    "name": "temperature",
    "value": temp,
    "user": 7
    }
    url = "http://127.0.0.1:8000/IOT/particularsensorupdate/12/"
    try:
        response = requests.put(url, json=data)
        if response.status_code == 200:
            pass
        else:
            print("Error:", response.status_code)
    except:
        print("Error: Cannot Connect Backend Server")

#soil moisture value update in database
def put_soil(soil):
    data = {
    "pk": 13,
    "name": "moisture",
    "value": soil,
    "user": 7
    }
    url = "http://127.0.0.1:8000/IOT/particularsensorupdate/13/"

    try:
        response = requests.put(url, json=data)
        if response.status_code == 200:
            pass
        else:
            print("Error:", response.status_code)
    except:
        print("Error: Cannot Connect Backend Server")

#humidity value update in database
def put_humi(humi):
    data = {
    "pk": 14,
    "name": "humidity",
    "value": humi,
    "user": 7
    }
    url = "http://127.0.0.1:8000/IOT/particularsensorupdate/14/"
    try:
        response = requests.put(url, json=data)
        if response.status_code == 200:
            pass
        else:
            print("Error:", response.status_code)
    except:
        print("Error: Cannot Connect Backend Server")


while True:
    temp = fetch_temp_data()
    humi = fetch_humidity_data()
    soil = fetch_soil_moisture_data()

    if temp != None:
        temp = float(temp)
        put_temp(temp)

    if humi != None:
        humi = float(humi)
        put_humi(humi)

    if soil != None:
        soil = float(soil)
        put_soil(soil)

    print("Temp: ", temp, "  Humi: ", humi, "  Soil: ", soil)

    time.sleep(30)