# crawling_KBS.py
# 네이버 로그인 시 아이디/비밀번호를 문자 단위로 타이핑하도록 구현
# PEP 8 규칙과 제약사항을 준수함

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time


class NaverCrawler:
    def __init__(self, driver_path, user_id, user_pw):
        # 드라이버 경로, 사용자 계정 정보 초기화 부분임
        self.driver_path = driver_path
        self.user_id = user_id
        self.user_pw = user_pw
        self.driver = None
        self.contents = []

    def start_driver(self):
        # Service 객체를 이용해 크롬 드라이버 실행
        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service)

    def type_speed(self, element, text, type_delay=0.):
        # element: selenium element, text: 입력 문자열, type_delay: 문자 사이 지연(초)
        for ch in text:
            element.send_keys(ch)
            time.sleep(type_delay)

    def login(self):
        # 네이버 로그인 페이지 이동
        self.driver.get('https://nid.naver.com/nidlogin.login')
        time.sleep(2)

        # 아이디 입력 (문자 단위로)
        id_box = self.driver.find_element(By.ID, 'id')
        id_box.clear()
        # type_delay 값을 조절하면 더 천천히 혹은 빠르게 타이핑 가능
        self.type_speed(id_box, self.user_id, type_delay=1)
        time.sleep(0.3)

        # 비번 입력 (문자 단위로)
        pw_box = self.driver.find_element(By.ID, 'pw')
        pw_box.clear()
        self.type_speed(pw_box, self.user_pw, type_delay=1)
        time.sleep(0.3)

        # 로그인 버튼 클릭
        login_btn = self.driver.find_element(By.ID, 'log.login')
        login_btn.click()
        time.sleep(3)

    def crawl_contents(self):
        # 로그인 후 메인 페이지 이동
        self.driver.get('https://www.naver.com/')
        time.sleep(3)

        # 예시: 로그인 사용자만 보이는 메일 영역 텍스트 수집
        try:
            mail_area = self.driver.find_element(By.CSS_SELECTOR, 'a.link_mail')
            self.contents.append(mail_area.text)
        except Exception:
            self.contents.append('로그인 사용자 전용 콘텐츠를 찾을 수 없음')

    def show_contents(self):
        # 수집한 콘텐츠 출력
        print(self.contents)

    def quit(self):
        # 종료
        if self.driver:
            self.driver.quit()


def main():
    # 실제 아이디 비번 (여기만 실제 값으로 바꿔주세요)
    user_id = 'qwer'
    user_pw = '1234'

    # 드라이버 절대경로: 실제 chromedriver 위치로 수정하세요
    driver_path = r'C:\Users\dino1\codyssey\qwer\chromedriver.exe'

    crawler = NaverCrawler(driver_path, user_id, user_pw)
    crawler.start_driver()
    crawler.login()
    crawler.crawl_contents()
    crawler.show_contents()
    crawler.quit()


if __name__ == '__main__':
    main()
