import json
import requests
import urllib.parse


class routing:
    def getDist(address1,address2):
        URL = "http://www.mapquestapi.com/directions/v2/route?key={}"

        API_KEY = "4Xqu5BaLEqresGWOOxEAsw5EKshw48OP"

        PAYLOAD = {"locations" : [
                        address1,
                        address2
                    ],
                    "options": {
                        "unit": "k"
                    }
                  }
        # print(json.dumps(PAYLOAD, indent=4, sort_keys=True))
        r = requests.post(URL.format(API_KEY), json=PAYLOAD)
        r.json()
        rDict = json.loads(r.text)
        # print(rDict)
        # print(json.dumps(rDict, indent=4, sort_keys=True))
        dist = rDict["route"]["distance"]
        return dist

    def getTime(address1,address2):
        URL = "http://www.mapquestapi.com/directions/v2/route?key={}"

        API_KEY = "4Xqu5BaLEqresGWOOxEAsw5EKshw48OP"

        PAYLOAD = {"locations" : [
                        address1,
                        address2
                    ],
                    "options" : {
                        "unit" : "k"
                    }
                  }
        # print(json.dumps(PAYLOAD, indent=4, sort_keys=True))
        r = requests.post(URL.format(API_KEY), json=PAYLOAD)
        r.json()
        rDict = json.loads(r.text)
        # print(rDict)
        # print(json.dumps(rDict, indent=4, sort_keys=True))
        time = rDict["route"]["formattedTime"]
        return int(time[3:5])