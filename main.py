import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
# from emoji import emojize


# 드라이버 설치
# https://jlim0316.tistory.com/225


def setChrome(location):
    global chrome
    chrome = webdriver.Chrome(executable_path=r"" + location)

    global ac
    ac = ActionChains(chrome)

    #붙혀넣기
    ac.key_down(Keys.COMMAND).send_keys('v').key_up(Keys.CONTROL) # todo 윈도우는 컨트롤로 바꾸기

    #  메시지 내용
    # ac.send_keys("안녕하세요. 저희는 인디 아티스트의 자작곡 음원을 전문으로 소개하고 팬덤 형성을 돕는 플랫폼 ‘스몰웨이브’ 입니다.")
    # ac.key_down(Keys.SHIFT).send_keys(Keys.ENTER).send_keys(Keys.ENTER).key_up(
    #     Keys.SHIFT)  # Shift 누르고 > Enter 보내고 > Shift 떼고
    # ac.send_keys("게시 음원에 대한 스트리밍 기능과 팬카페 등의 각종 커뮤니티 기능을 통해 인디 아티스트가 일반 대중과 밀접하게 소통할 수 있도록 지원합니다.")
    # ac.key_down(Keys.SHIFT).send_keys(Keys.ENTER).send_keys(Keys.ENTER).key_up(
    #     Keys.SHIFT)  # Shift 누르고 > Enter 보내고 > Shift 떼고
    # ac.send_keys("2022년 10월 4일 10시 임시 오픈 예정이니, 저희 홈페이지(https://www.smallwave.co.kr/)에 오셔서 자작곡 음원을 마음껏 게시해 주시기 바랍니다.")
    # ac.key_down(Keys.SHIFT).send_keys(Keys.ENTER).send_keys(Keys.ENTER).key_up(
    #     Keys.SHIFT)  # Shift 누르고 > Enter 보내고 > Shift 떼고
    # ac.send_keys("감사합니다.")
    # ac.key_down(Keys.SHIFT).send_keys(Keys.ENTER).send_keys(Keys.ENTER).key_up(
    #     Keys.SHIFT)  # Shift 누르고 > Enter 보내고 > Shift 떼고
    # ac.send_keys("스몰웨이브 ⭐ ✊") # 유니코드 네자리 이상은 오류 있음 즉, 유니코드FFFF 이상은 에러

def move(url):
    chrome.get(url)
    time.sleep(3 + random.random())

def login(username, your_password):

    usern = chrome.find_element(By.NAME, "username")
    usern.send_keys(username)

    passw = chrome.find_element(By.NAME, "password")
    passw.send_keys(your_password)

    # 로그인 확인 버튼 누르기
    doLogin = chrome.find_element(By.CLASS_NAME, "sqdOP.L3NKy.y3zKF")
    doLogin.click()
    time.sleep(5+ random.random())

    # 로그인 데이터 저장하기 버튼
    saveLoginDataBtn = chrome.find_element(By.CLASS_NAME, "_acan._acap._acas")
    saveLoginDataBtn.click()
    time.sleep(3+ random.random())

def sendMessage(targetId):
    # 로그인 버튼이 있는 경우 비공계 계정s
    try:
        chrome.find_element(By.CLASS_NAME, '_aa_u')
        print(f"===경고(비공개 계정): {targetId}") # 비공개 계정입니다.
        return 2
    except:
        pass

    try:
        messageBtn = chrome.find_element(By.CLASS_NAME, '_acan._acap._acat')  # 메시지 전송 버튼
        messageBtn.click()
        time.sleep(3 + random.random())
    except:
        print(f"===경고 (메시지 차단): {targetId}")
        return 3

    # 알림 설정 하기 얼럿 있는지 체크
    try :
        chrome.find_element(By.CLASS_NAME, '_a9--._a9_1').click()  # 얼럿 닫기
        time.sleep(1 + random.random())
    except:
        # 알림 설정 얼럿이 없음
        pass

    try:
        mbox = chrome.find_element(By.TAG_NAME, 'textarea')
        mbox.click()
        ac.perform() # 키체인 내용 실행
        time.sleep(1 + random.random())
        mbox.send_keys(Keys.RETURN) #  내용 보내기
        return 1
    except:
        print(f"===실패(매시지 전송 도중 오류 발생): {targetId}")
        return 0

def runMecro():
    username = "01044890709"#'id'  # 로그인할 인스타 아이디 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    password = "guswndi801!"#'pw'  # 로그인할 인스타 비밀번호  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    triedCount = 0
    sendCount = 0
    secretIdCount = 0
    blockCount = 0

    global idList
    idList = []

    # 파일 읽기
    filePath = os.getcwd()
    file = open(filePath+"/insta_id_list.txt", "r") #!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    idListStr = file.read()
    idListStr=idListStr.replace("[","")
    idListStr=idListStr.replace("]","")
    idListStr=idListStr.replace("'","")
    idListStr = idListStr.replace(" ", "")
    idList = idListStr.split(",")

    isFirst = True
    for id in idList:
        triedCount += 1
        # 첫 실행
        if isFirst :
            print(filePath)
            setChrome(filePath+"/chromedriver")
            move('https://www.instagram.com/')
            login(username, password)
            isFirst = not isFirst # 1회 끝

        print(f"전송 중인 계정 : {id}")
        url = 'https://www.instagram.com/' + id  # 메시지 보낼 인스타 아이디
        move(url)
        result = sendMessage(id)
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
        elif result == 3:
            # 메시지 차단 계정
            blockCount += 1

    print(f"파일 내에 존재하는 계정 수 : {len(idList)}")
    print(f"전송 시도한 총 계정 수 : {triedCount}")
    print(f"비공개 계정으로 실패 : {secretIdCount}")
    print(f"메시지 차단으로 실패 : {blockCount}")
    print(f"전송 성공한 계정 수 : {sendCount}")
    file.closed
    # chrome2.close()

def pushEmoji( strName):
    chrome.find_element(By.CLASS_NAME, '_abl-').click()

    if strName == "smile":
        chrome.find_element(By.CLASS_NAME, '_acan. _acao._acas').click()
    if strName == "arrow":
        chrome.find_element(By.CSS_SELECTOR, 'body>div:nth-child(60)>div>div>div>div._aa61>div>div>div:nth-child(140)>div>div>div').click()
        chrome.find_element(By.CSS_SELECTOR, '#polaris-emoji-variation-👉').click()
    if strName == "idea":
        chrome.find_element(By.CLASS_NAME, '_acan _acao _acas').click()


    pass

if __name__ == '__main__':
    runMecro()
