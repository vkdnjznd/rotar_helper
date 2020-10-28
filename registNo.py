import json
import requests
import re
from urllib import parse
from regionCode import getRegionCode

URL = "http://openapi.1365.go.kr/openapi/service/rest/VolunteerPartcptnService/getVltrAreaList"
API_KEY = "YOUR_API_KEY"

# return volunteer program registnumber dictionary for each region
def getRegistNo(gugunDict):
    programDict = {}

    for nm, gugunCd in gugunDict.items():
        programList = []
        params = {'schSido': '6110000', 'schSign1': gugunCd,
                'ServiceKey': API_KEY, '_type': 'json', 'numOfRows': '1000'}
        resp = requests.get(URL, params=params)
        data = resp.json()

        try:
            items = data['response']['body']['items']['item']
        except:
            continue

        if type(items) != list:
            programNo = items['progrmRegistNo']
            programList.append(programNo)
        else:
            for item in items:
                programNo = item['progrmRegistNo']
                programList.append(programNo)
        
        programDict[nm] = programList

    return programDict
