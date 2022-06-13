#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import socket
from _thread import *
import threading

lock = threading.Lock() #뮤텍스를 위한 변수

# 도시(sidoName)에 따른 미세먼지와 초미세먼지 정보를 받는 메소드
def getFinedust(sidoName):
    url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty' #api url
    service_key = 'FGXCM8tLTAxT2Za5jgauMH1Iw3f8Lsob/GfyVfFV4yIzWdg/HA/cEoDY+szZ+A+qbQZOHjGQfCE9SOLAnbt1cA==' #api 서비스키
    
    #api 요청에 필요한 정보 담기
    params ={'serviceKey' : service_key, 'returnType' : 'json', 'numOfRows' : '1', 
            'pageNo' : '1', 'sidoName' : sidoName, 'ver' : '1.3' }
    
    #api 호출하기
    response = requests.get(url, params=params)
    items = response.json().get('response').get('body').get('items')[0] #items의 구조 -> [{키:값 ...}]
    
    #정보 추출
    finedust_data = dict() #미세먼지 정보를 담은 딕셔너리
    finedust_data['sidoName'] = sidoName #도시 정보 담기

    #여러 정보 중 미세먼지와 초미세먼지의 정보만 추출
    finedust_data['pm10Value'] = items['pm10Value'] #미세먼지 농도
    finedust_data['pm25Value'] = items['pm25Value'] #초미세먼지 농도

    pm10Grade1h_code = items['pm10Grade1h'] #미세먼지 등급
    if pm10Grade1h_code == '1':
        pm10Grade1h_state = '좋음'
    elif pm10Grade1h_code == '2':
        pm10Grade1h_state = '보통'
    elif pm10Grade1h_code == '3':
        pm10Grade1h_state = '나쁨'
    else:
        pm10Grade1h_state = '매우나쁨'
    finedust_data['pm10Grade1h_state'] = pm10Grade1h_state

    pm25Grade1h_code = items['pm25Grade1h'] #초미세먼지 등급
    if pm25Grade1h_code == '1':
        pm25Grade1h_state = '좋음'
    elif pm25Grade1h_code == '2':
        pm25Grade1h_state = '보통'
    elif pm25Grade1h_code == '3':
        pm25Grade1h_state = '나쁨'
    else:
        pm25Grade1h_state = '매우나쁨'   
    finedust_data['pm25Grade1h_state'] = pm25Grade1h_state
    
    return finedust_data

# 쓰레드에서 실행되는 코드: 접속 클라이언트마다 새 쓰레드가 생성되어 통신
def threaded(client_socket, addr):
    print('Connected by ', addr[0] , addr[1])

    while True:
        data = client_socket.recv(1024)
        if not data:
            print('Disconnected by ' , addr[0], addr[1])
            break
        print('Received from ' ,addr[0],addr[1],'recv data:', data)
        data = data.decode()

        lock.acquire()
        if(data == "0"): sido = "전국"
        elif(data == "1"): sido = "서울"
        elif(data == "2"): sido = "부산"
        elif(data == "3"): sido = "대구"
        elif(data == "4"): sido = "인천"
        elif(data == "5"): sido = "광주"
        elif(data == "6"): sido = "대전"
        elif(data == "7"): sido = "울산"
        elif(data == "8"): sido = "경기"
        elif(data == "9"): sido = "강원"
        elif(data == "10"): sido = "충북"
        elif(data == "11"): sido = "충남"
        elif(data == "12"): sido = "전북"
        elif(data == "13"): sido = "전남"
        elif(data == "14"): sido = "경북"
        elif(data == "15"): sido = "경남"
        elif(data == "16"): sido = "제주"
        elif(data == "17"): sido = "세종"
        
        finedust = getFinedust(sido) #미세먼지 정보 받기
        
        msg = ("<"+finedust['sidoName']+"의 미세먼지 정보> 미세먼지:"+finedust['pm10Grade1h_state']+ 
            "("+finedust['pm10Value']+"), 초미세먼지:"+finedust['pm25Grade1h_state']+
            "("+finedust['pm25Value']+")")
           
        client_socket.send(msg.encode('utf-8'))
        lock.release() 

    client_socket.close()


HOST = '127.0.0.1'
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))

server_socket.listen(1)

print('start server!')

# 클라이언트가 접속하면 accept 함수에서 새로운 소켓을 리턴
# 새 쓰레드에서 해당 소켓을 사용하여 통신
while True:
    print('waiting...')
    client_socket, addr = server_socket.accept()
    start_new_thread(threaded, (client_socket, addr))

server_socket.close()