import json
import requests
import re
import time
import pandas as pd
import sys, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from openpyxl import load_workbook


def getLocation(organDict):
    locDict = {}
    locations = []
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # 인터페이스 없는
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome("chromedriver", options=options)
    driver.get("https://www.google.co.kr/maps")
    driver.implicitly_wait(1.5)
    for gugunnm, organSet in organDict.items():
        for organ in organSet:    
            inputbox = driver.find_element_by_id("searchboxinput")
            inputbox.send_keys(organ)
            driver.implicitly_wait(1.5)
            driver.find_element_by_id("searchbox-searchbutton").click()
            driver.implicitly_wait(1)
            time.sleep(5)
            inputbox.clear()
            driver.implicitly_wait(1)
            try:
                driver.find_element_by_class_name("section-hero-header-title-description")
                driverUrl = driver.current_url
                html = driver.page_source
                soup = bs(html, "html.parser")
                addr = soup.find("div", {'data-section-id' : 'ad'}).text
                addr = addr.strip()
            except:
                continue
            
            if gugunnm not in addr:
                continue

            regex = re.compile("[/]@[\d]*.*[\d][,$]")
            matched = regex.search(driverUrl)
            loc_in_str = matched.group()

            loc_in_str = loc_in_str[2:]
            location = loc_in_str[:-1].split(',')
            locations.append(location)

        locDict[gugunnm] = locations

    driver.quit()

    # naver map과 좌표 순서가 반대
    return locDict


def getDuration(goal_px, goal_py):
    URL = "https://map.naver.com/v5/api/dir/findpt"

    # 역곡역 좌표
    start_px = '126.8115389'
    start_py = '37.4851381'

    params = {'start': start_px + ',' + start_py, 'goal' : goal_px + ',' + goal_py, 'crs' : 'EPSG:4326', 
                'isStatic' : 'true', 'mode' : 'STATIC', 'lang' : 'ko'}

    resp = requests.get(URL, params=params)
    data = resp.json()

    return data['staticPaths'][0]['duration']

    
def getOrganDict(gugun):
    # MAX_VOLUN_CNT = 15
    organDict = {}
    URL = "https://www.vms.or.kr/partspace/recruit.do"

    organList = []
    gugunnm = ""

    # params = {'area' : '0101', 'areagugun' : gugun, 'sttdte' : '2015-01-01', 'enddte' : '2020-12-31',
    #         'searchType' : 'title', 'page' : '1'}

    # resp = requests.get(URL, params=params)
    # html = resp.text
    # soup = bs(html, "html.parser")

    # 최대 PAGE 계산 --> 페이지 응답시간이 너무 느림
    # total_volun_cnt = soup.find("p", class_ = "total").find("span").get_text()
    # page_limit = int(total_volun_cnt) // MAX_VOLUN_CNT

    for page in range(1, 101):
        if page % 5 == 0:
            print("현재 {} 페이지 진행중... {} 개 추출완료\n".format(page, len(organList)))
        
        params = {'area' : '0104', 'areagugun' : gugun, 'sttdte' : '2015-01-01', 'enddte' : '2020-12-31',
            'searchType' : 'title', 'page' : page}

        resp = requests.get(URL, params=params)
        html = resp.text
        soup = bs(html, "html.parser")

        if not gugunnm:
            gugunnm = soup.find("select", {'name' : 'areagugun'}).find("option", {'value' : gugun}).get_text()
        
        volunList = soup.find("ul", class_ = "list_wrap").parent.find_all("dl")
        for volun in volunList:
            html_dtdl = re.search("<dt>모집기관:<[/]dt>\n<dd>.*<[/]dd>", str(volun))
            if html_dtdl:
                html_dd = re.search("<dd>.*<[/]dd>", html_dtdl.group())
                organ_name = re.sub("<.+?>", '', html_dd.group(), 0)
                organList.append(organ_name)
    
    organDict[gugunnm] = set(organList)

    return organDict

def getCurrentdir():
    dir_path = os.path.dirname(sys.argv[0])
    current_path = os.path.abspath(dir_path)

    return current_path

def save_to_xlsx(data, temp=False):
    data_path = '\\data\\duration.xlsx'
    data_xlsx = getCurrentdir() + data_path

    d = {'지역' : [data[0]], '소요시간' : [data[1]], '표본개수' : [data[2]]}
    df = pd.DataFrame.from_dict(d, orient='columns')

    if temp:
        temp_path = '\\data\\{}.xlsx'.format(data[0])
        temp_path = getCurrentdir() + temp_path
        df.to_excel(temp_path, index=False)
    else:
        if not os.path.isfile(data_xlsx):
            df.to_excel(data_xlsx, index=False)
        else:
            writer = pd.ExcelWriter(data_xlsx, engine='openpyxl')
            writer.book = load_workbook(data_xlsx)
            writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
            reader = pd.read_excel(data_xlsx)
            df.to_excel(writer, startrow=len(reader) + 1, index=False, header=False)
            
            writer.close()

    
if __name__ == "__main__":
    seoul_gugunlist = ['1111000000', '1114000000', '1117000000', '1120000000', '1121500000',
                    '1123000000', '1126000000', '1129000000', '1130500000', '1132000000',
                    '1135000000', '1138000000', '1141000000', '1144000000', '1147000000',
                    '1150000000', '1153000000', '1154500000', '1156000000', '1159000000',
                    '1162000000', '1165000000', '1168000000', '1171000000', '1174000000']
    
    inchoen_gugunlist = ['2811000000', '2814000000', '2817700000', '2818500000', '2820000000',
                        '2823700000', '2824500000', '2817700000', '2826000000', '2871000000', '2872000000']
    
    for gugun in seoul_gugunlist:
        avg_min = 0
        save_data = []
        organDict = getOrganDict(gugun)
        locDict = getLocation(organDict)
        for gugunnm, locations in locDict.items():
            print("현재 {} 저장 시작".format(gugunnm))
            for loc in locations:
                minute = getDuration(loc[1], loc[0])
                avg_min += minute
            
            if not locations:
                continue

            avg_min = avg_min / len(locations)
            save_data = [gugunnm, avg_min, len(locations)]
            save_to_xlsx(save_data)
            print("현재 {} 완료".format(gugunnm))
