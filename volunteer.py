import json
import requests
import re
import time
import sys, os
from urllib import parse
from bs4 import BeautifulSoup as bs
from regionCode import getRegionCode
from registNo import getRegistNo


def getItemList(sidoName):
    URL = "http://openapi.1365.go.kr/openapi/service/rest/VolunteerPartcptnService/getVltrPartcptnItem?"
    API_KEY = "YOUR_API_KEY"

    gugundict = getRegionCode(sidoName)
    programdict = getRegistNo(gugundict)
    volitem = []

    for gugunnm, programlist in programdict.items():
        for program in programlist:
            params = {'_type' : 'json', 'progrmRegistNo' : program}
            resp = requests.get(URL, params=params)
            data = resp.json()
            resultCode = data['response']['header']['resultCode']
            isAdult = data['response']['body']['items']['item']['adultPosblAt']
            volState = data['response']['body']['items']['item']['progrmSttusSe']

            # response 에러 혹은 성인불가 봉사, 모집완료 봉사 제외
            if resultCode != '00' or isAdult == 'N' or volState == 3:
                continue
            
            try:
                item = data['response']['body']['items']['item']
                # 등록번호, 지역, 제목, 모집인원, 봉사활동 시작 날짜, 끝 날짜, 시작 시간, 끝 시간
                volInfo = [item['progrmRegistNo'], item['nanmmbyNm'], item['progrmSj'],
                            item['rcritNmpr'], item['progrmBgnde'], item['progrmEndde'],
                            item['actBeginTm'], item['actEndTm']]

                volitem.append(volInfo)
            except:
                pass

    print(volitem)


if __name__ == "__main__":
    getItemList("서울")
    getItemList("인천")