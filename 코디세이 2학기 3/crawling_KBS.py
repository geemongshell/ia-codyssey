# crawling_KBS.py
# KBS 뉴스 메인 페이지에서 실제 헤드라인 뉴스 가져오기
# 제약: Python 3.x, requests만 외부 사용, PEP 8 준수

import requests
from bs4 import BeautifulSoup  # 외부 패키지 필요


class KbsCrawler:
    """KBS 뉴스 주요 헤드라인 크롤러 클래스"""

    def __init__(self, url):
        self.url = url
        self.headlines = []

    def fetch_page(self):
        """웹 페이지를 요청해서 HTML을 반환한다."""
        try:
            response = requests.get(self.url)
        except requests.RequestException as err:
            print(f'웹 요청 중 오류 발생: {err}')
            return None

        if response.status_code == 200:
            return response.text
        print(f'HTTP 상태 코드: {response.status_code}')
        return None

    def parse_headlines(self, html):
        """HTML에서 헤드라인 뉴스 텍스트들을 추출한다."""
        soup = BeautifulSoup(html, 'html.parser')

        # 아래 선택자는 개발자 도구로 확인한 실제 값에 따라 조정 필요
        # 예시 선택자:
        #   메인 뉴스 영역 div: class="main_news" (가정)
        #   뉴스 제목 a 태그: class="tit" 또는 태그 내 <a> 직접
        main_news_div = soup.find('div', class_='main_news')
        if main_news_div:
            # 예: <a class="tit">제목</a>
            anchors = main_news_div.find_all('a', class_='tit')
            for a in anchors:
                text = a.get_text(strip=True)
                if text:
                    self.headlines.append(text)

        # 대체 선택자: 만약 위가 실패할 경우
        if not self.headlines:
            # 예: 주요 뉴스들이 <h2 class="title"> 또는 <h3 class="title"> 로 감싸져 있을 수 있다
            title_tags = soup.find_all(['h2', 'h3'], class_='title')
            for tag in title_tags:
                text = tag.get_text(strip=True)
                if text:
                    self.headlines.append(text)

        # 또 다른 대체: <a> 태그만으로 제목 추출
        if not self.headlines:
            # 뉴스 링크가 많은 <a> 태그 중 특정 위치의 것들을 가져올 수 있다
            anchors = soup.find_all('a')
            for a in anchors:
                text = a.get_text(strip=True)
                # 너무 짧거나 공백이면 걸러내기
                if text and len(text) > 20:
                    self.headlines.append(text)
            # 중복 제거
            self.headlines = list(dict.fromkeys(self.headlines))

    def get_headlines(self):
        """헤드라인 리스트 반환"""
        return self.headlines


def main():
    url = 'https://news.kbs.co.kr/news/pc/main/main.html'
    crawler = KbsCrawler(url)

    html = crawler.fetch_page()
    if html:
        crawler.parse_headlines(html)
        headlines = crawler.get_headlines()

        print('=== KBS 뉴스 메인 헤드라인 ===')
        if headlines:
            for idx, title in enumerate(headlines, 1):
                print(f'{idx}. {title}')
        else:
            print('헤드라인을 찾지 못했습니다.')
    else:
        print('웹 페이지를 불러오지 못했습니다.')


if __name__ == '__main__':
    main()
