import json
import requests
from urllib import parse

URL = "http://openapi.1365.go.kr/openapi/service/rest/CodeInquiryService/getAreaCodeInquiryList?"
API_KEY = "YOUR_API_KEY"

# return region code dictionary
def getRegionCode(sidoName):
    gugunDict = {}

    params = {'schSido' : sidoName, 'ServiceKey' : API_KEY, '_type' : 'json', 'numOfRows' : '100'}
    params = parse.urlencode(params, doseq=True)

    resp = requests.get(URL+params)
    data = resp.json()
    items = data['response']['body']['items']['item']

    for item in items:
        gugunCd = item['gugunCd']
        gugunName = item['gugunNm']

        gugunDict[gugunName] = gugunCd
    
    return gugunDict

if __name__ == "__main__":
    gugunDict = getRegionCode("서울")
    print(gugunDict)    