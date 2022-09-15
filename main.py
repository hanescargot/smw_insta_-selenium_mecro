
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdrivermanager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions
import time
import random

# 드라이버 설치
# https://jlim0316.tistory.com/225


def setChrome(location):
    global chrome2
    chrome2 = webdriver.Chrome(executable_path=r''+location)
    time.sleep(1+random.random())

def move(url):
    chrome2.get(url)
    time.sleep(3 + random.random())

def login(username, your_password):

    usern = chrome2.find_element(By.NAME, "username")
    usern.send_keys(username)

    passw = chrome2.find_element(By.NAME, "password")
    passw.send_keys(your_password)

    # 로그인 확인 버튼 누르기
    doLogin = chrome2.find_element(By.CLASS_NAME,"sqdOP.L3NKy.y3zKF")
    doLogin.click()
    time.sleep(3+ random.random())

    # 로그인 데이터 저장하기 버튼
    saveLoginDataBtn = chrome2.find_element(By.CLASS_NAME,"sqdOP.L3NKy.y3zKF")
    saveLoginDataBtn.click()
    time.sleep(3+ random.random())

def sendMessage(targetId, msg):
    # 로그인 버튼이 있는 경우 비공계 계정s
    try:
        chrome2.find_element(By.CLASS_NAME, '_aa_u')
        print(f"===경고(비공개 계정): {targetId}") # 비공개 계정입니다.
        return 2
    except:
        pass

    try:
        messageBtn = chrome2.find_element(By.CLASS_NAME, '_acan._acap._acat')  # 메시지 전송 버튼
        messageBtn.click()
        time.sleep(3 + random.random())
    except:
        print(f"===실패(매시지 전송창 진입 도중 오류 발생): {targetId}")
        return 0

    # 알림 설정 하기 얼럿 있는지 체크
    try :
        chrome2.find_element(By.CLASS_NAME, '_a9--._a9_1').click()  # 얼럿 닫기
        time.sleep(1 + random.random())
    except:
        # 알림 설정 얼럿이 없음
        pass

    try:
        mbox = chrome2.find_element(By.TAG_NAME,'textarea')  # 텍스트 박스 입력
        mbox.send_keys(msg)
        time.sleep(1 + random.random())
        mbox.send_keys(Keys.RETURN) # 아마 내용 지우기 ?
        print(f"성공: {targetId}")
        return 1
    except:
        print(f"===실패(매시지 전송 도중 오류 발생): {targetId}")
        return 0

def runMecro():
    username = '01044890709'  # 로그인할 인스타 아이디 !!!!!!!!!!!!!!!!!!!!!
    password = 'guswndi801!'  # 로그인할 인스타 비밀번호  !!!!!!!!!!!!!!!!!!!
    sendCount = 0
    secretIdCount = 0

    global idList
    idList = []

    # 파일 읽기
    file = open("/Users/hyunjhan/Downloads/insta_id_list.txt", "r")
    idListStr = file.read()
    idListStr=idListStr.replace("[","")
    idListStr=idListStr.replace("]","")
    idListStr=idListStr.replace("'","")
    idListStr = idListStr.replace(" ", "")
    idList = idListStr.split(",")

    isFirst = True
    for id in idList:

        # 첫 실행
        if isFirst :
            setChrome('/Users/hyunjhan/Documents/xian_program_library/chromedriver')
            move('https://www.instagram.com/')
            login(username, password)
            isFirst = not isFirst # 1회 끝

        print(f"전송 중인 계정 : {id}")
        url = 'https://www.instagram.com/' + id  # 메시지 보낼 인스타 아이디
        move(url)
        result = sendMessage(id, f"매크로 작동 {sendCount}")
        if result == 0 :
            # 실패 - 코드가 완전히 멈춤
            print("!!!!!!!!!!!!!!!!!!!!!오류 확인하세요!!!!!!!!!!!!!!!!!!")
            break
        elif result == 1 :
            # 성공
            sendCount += 1
        elif result == 2 :
            # 비공개 계정
            secretIdCount += 1

    print(f"전송 시도한 총 계정 수 : {len(idList)}")
    print(f"비공개 계정으로 실패 : {secretIdCount}")
    print(f"전송 성공한 계정 수 : {sendCount}")
    file.closed
    # chrome2.close()


if __name__ == '__main__':
    runMecro()
