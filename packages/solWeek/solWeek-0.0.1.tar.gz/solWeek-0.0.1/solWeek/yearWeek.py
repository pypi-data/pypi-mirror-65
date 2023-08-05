#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 함수 기능: 숫자/문자 상관없이 입력한 주차(yearweek)에서 원하는만큼 주차수(minusWeek) 빼주는 함수
def preweek(yearweek, minusWeek):
    from isoweek import Week
# isoweek을 활용 -> 기능 둘러보기 https://pypi.org/project/isoweek/
# isoweek.Week(year, week)가 있음
# operations 지원하는 것을 찾음

# 1. 리스트 형태로 연도와 주차를 분리하기 위해 yearweek가 문자열이 아닌 경우 str로 캐스팅
    if type(yearweek) != str:
        yearweek = str(yearweek)
    minusWeek = int(minusWeek)
# 2. Week: 문자열은 지원 안 되는 것 확인함 -> int로 형변환 필요
# 3. Week의 출력형인 yyyyWww에서 W를 제거 -> str으로 캐스팅 후 replace 사용
# 4. 결과값인 result가 문자형으로 나와야 함 -> str으로 캐스팅
    result = str(Week(int(yearweek[:4]), int(yearweek[-2:]) - minusWeek)).replace("W","")
    return result

# 함수 기능: 입력한 주차(yearweek)에서 원하는만큼 주차수(plusWeek) 더해주는 함수
def postweek(yearweek, plusWeek):
    from isoweek import Week
    if type(yearweek) != str:
        yearweek = str(yearweek)
    plusWeek = int(plusWeek)
    result = str(Week(int(yearweek[:4]), int(yearweek[-2:]) + plusWeek)).replace("W","")
    return result

