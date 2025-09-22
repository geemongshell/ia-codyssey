import requests
from bs4 import BeautifulSoup  # 외부 패키지 필요하다 해서 다운로드함


class KbsCrawler:
    """KBS 뉴스 주요 헤드라인 크롤러 클래스"""

    def __init__(self, url):
        self.url = url
        self.headlines = []

    def fetch_page(self):
        #웹 페이지를 요청해서 HTML을 반환하는 부분
        try:
            response = requests.get(self.url) #넷웤 시도
        except requests.RequestException as err:
            print(f'웹 요청 중 오류 발생: {err}')
            return None #안되면 ㅈㅈ

        if response.status_code == 200:
            return response.text
        print(f'HTTP 상태 코드: {response.status_code}')
        return None #만약 가져오는데 성공하면 페이지 가져오는거 

    def parse_headlines(self, html):
        #HTML에서 헤드라인 뉴스 텍스트들을 추출한다.
        soup = BeautifulSoup(html, 'html.parser')


        # 대체 선택자: 만약 위가 실패할 경우
        if self.headlines:
            # 예: 주요 뉴스들이 <p class="title"> 로 감싸져 있을 수 있다
            title_tags = soup.find_all(['p'], class_='title')
            for tag in title_tags:
                text = tag.get_text(strip=True)
                if text:
                    self.headlines.append(text)

        # 18 일단 야매: <a> 태그만으로 제목 추출
        if not self.headlines:
            # 그냥 싹 다 가져와
            anchors = soup.find_all('a')
            for a in anchors:
                text = a.get_text(strip=True)
                # 너무 짧거나 공백이면 걸러내기
                if text and len(text) > 20:
                    self.headlines.append(text)
                    
                    
            # 중복 제거
            self.headlines = list(dict.fromkeys(self.headlines))

    def get_headlines(self):
        #헤드라인 리스트 반환
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
