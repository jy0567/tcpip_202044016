#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

HOST = '127.0.0.1'
PORT = 8080
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# 클라이언트 문자열을 서버로 전송 후, 서버에서 돌려준 메시지를 화면에 출력
# 'quit' 입력할 때까지 반복

sido = "전국(0), 서울(1), 부산(2), 대구(3), 인천(4), 광주(5), 대전(6), 울산(7), 경기(8), 강원(9), 충북(10), 충남(11), 전북(12), 전남(13), 경북(14), 경남(15), 제주(16), 세종(17)"
print("<미세먼지 농도 알림이>\n"+sido)
print("=========================================================================\n")

while True:
  message = input('조회하고 싶은 도시의 번호를 입력해주세요.(exit: "quit") : ')
  
  if (message == 'quit'):
    break

  client_socket.send(message.encode())
  data = client_socket.recv(1024)
  print(repr(data.decode()))

print("미세먼지 알림이를 이용해주셔서 감사합니다!")
client_socket.close()