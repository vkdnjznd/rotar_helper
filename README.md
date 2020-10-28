### 봉사 지역 찾기
봉사 동아리에서 적절한 봉사지역을 찾기 위해 역곡역을 기준으로 각 지역마다의 이동시간을 구한다 

<hr/>


### 각 소스파일의 설명</br>


- regionCode.py --> 공공데이터 API를 이용하여 각 지역의 구군코드를 가져온다</br>


- registNo.py --> 공공데이터 API를 이용하여 각 지역의 봉사 프로그램 리스트를 가져온다</br>


- duration.py --> 구한 봉사 프로그램들의 봉사 기관들의 주소를 selenium을 통해 구글 맵에 검색하여 좌표를 얻고, 그 좌표를 네이버 지도에 넘겨줌으로써 지역별 대중교통을 통한 이동시간을 구한다
<br/><br/>
<hr/>

### 지역별 데이터

##### data 폴더를 참조


![image](https://github.com/vkdnjznd/rotar_helper/blob/master/doc/data1.jpg)


![image](https://github.com/vkdnjznd/rotar_helper/blob/master/doc/data2.jpg)

<br/>
필요 라이브러리는 requirements.txt 를 참조


