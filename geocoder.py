import json
import requests
import urllib.parse


class geocoder:
    def getLatLng(address):
        URL = "http://www.mapquestapi.com/geocoding/v1/address?key={}&location={}"

        API_KEY = "4Xqu5BaLEqresGWOOxEAsw5EKshw48OP"

        r = requests.get(URL.format(API_KEY,urllib.parse.quote(address)))
        r.json()
        rDict = json.loads(r.text)
        # print(json.dumps(rDict, indent=4, sort_keys=True))
        # print(r.status_code)
        # print(r.reason)
        results = rDict["results"][0]
        locations = results["locations"][0]
        latLng = locations["latLng"]
        # lat = latLng["lat"]
        # lng = latLng["lng"]
        # print(address)
        # print("Lat, Lng: %s, %s" % (lat,lng))
        # print("---")
        return latLng


