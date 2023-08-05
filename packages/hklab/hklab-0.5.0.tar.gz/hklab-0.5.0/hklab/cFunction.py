#!/usr/bin/env python
# coding: utf-8

# In[1]:


def roundFunction(invalue):
    step1 = invalue * 1000
    step2 = int(step1)
    outvalue = step2/1000
    return outvalue

def roundFunction2(invalue):
    step1 = invalue * 1000
    step2 = int(step1)
    outvalue = step2/1000
    return outvalue

# 내용: 함수는 타입에 상관없이 list내 합계를 구함
# 파라미터(입력/출력): sampleList : List
# 목적: 문자열이든 숫자든 상관없이 합계 산출
# Step1: 합계 산출할 변수 선언
# Step2: 반복문을 통해 리스트 내 아이템 값을 누적함
# Step3: 누적결과 리턴
def listCalc (sampleList, inOption):
    # 입력파라미터
#     sampleList = ["11","22","33"]
#     # 0: 합 1: 곱
#     inOption = 0

    # 로직
    sampleListLen = len(sampleList)
    totalResult = 0

    for i in range(0, sampleListLen):
        eachItem = int(sampleList[i])
        # option 1:곱 0: 합
        if inOption == 1:
            if i == 0:
                totalResult = 1
            totalResult = totalResult * eachItem
        else:
            totalResult = totalResult + eachItem
    return totalResult

