import os

import pickle
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

import utils
import episode

# NaverWebtoonCrawler클래스는 리스트를 가져오는 역할을 하는 클래스
class NaverWebtoonCrawler:
    def __init__(self, webtoon_title=None):
        webtoon_search_result = self.find_webtoon(webtoon_title) #전체 웹툰 중에서 클래스 인자로 전달된 webtoon_title과 일치하는 웹툰의 정보가 담긴 리스트를 반환
        while not webtoon_search_result: #클레스 인자가 전달되지 않아서 webtoon_search_result 리스트의 인자가 0개일 경우 / 말하자면 검색결과가 없을 경
            search_title = input('검색할 웹툰명을 입력해주세요: ')
            webtoon_search_result = self.find_webtoon(search_title)
        # if문 안에서는 해당 웹툰을 고르게 되고, 헤당 웹툰에 대한 정보를 self.weboon에 담게 된다.
        if len(webtoon_search_result) ==1:
            self.webtoon = webtoon_search_result[0]
        elif len(webtoon_search_result) >= 2:
            while True:
                print('웹툰을 선택해주세요')
                for index, webtoon in enumerate(webtoon_search_result):
                    print('{}. {}'.format(index + 1, webtoon.title))
                try:
                    selected_index = int(input('-선택:'))
                    self.webtoon = webtoon_search_result[selected_index - 1]
                    break
                except IndexError:
                    print('에러] {}번 이하의 숫자를 선택해주세요\n'.format(
                        len(webtoon_search_result)
                    ))
                except ValueError:
                    print('에러] 헤당 웹툰의 숫자를 입력해주세요\n')
        self.episode_list = list()
        self.load(init=True)
        print('-현재 웹툰: %s' % self.webtoon.title)
        print('-로드된 Episode수: %s' % len(self.episode_list))
        print('-최신 에피소드: %s' % self.print_recent_episode_num())

        choice = input(f"\n선택한 웹툰'{self.webtoon.title}'을 다운 받으시겠습니까? \n\n ---- 해당되는 번호를 입력해주세요 ---- \n\n1.전체다운\n2.최신화 다운\n3.취소\n 입력 : ")
        if int(choice) == 1:
            print('전체다운 선택 선택')
            self.update_episode_list()
            self.save_all_episode_image()
        elif int(choice) == 2:
            print('최신화 다운 선택')
            self.save_recent_episode_image()
            pass
        else :
            print('취소')
            pass
    # self.webtoon에 해당하는 실제 웹툰의 총 episode
    @property
    def total_episode_count(self):
        el = utils.get_webtoon_episode_list(self.webtoon)
        return int(el[0].no)

    @property
    def up_to_date(self):
        return len(self.episode_list) == self.total_episode_count

    def find_webtoon(self, title):
        # results = []
        # webtoon_list = self.get_webtoon_list()
        # for webtoon in webtoon_list:
        #     if title in webtoon.title:
        #         results.append(webtoon)
        # return results
        # get_webtoon_list() 메서드를 순회하며(전체 웹툰 기본정보도 자동 업데이트 됨) 인자로 전달된
        # title과 웹툰의 이름(webtoon.title)이 일치 할 경우 일치하는 웹툰의 기본 정보가 담긴
        # 튜플의 리스트를 반환
        return [webtoon for webtoon in self.get_webtoon_list() if title in webtoon.title]

    def get_webtoon_list(self):
        # 요일 웹툰 전체가 나와있는 페이지 에서 각각의 웹툰의
        # 고유 넘버(title_id), thumbnail url(img_url), 웹툰의 제목(title)을
        # 네임드 튜플변수에(webtoon) 할당하고 webtoon_list에 추가해서
        # 웹툰 이름(title)순으로 정리된 webtoon_list를 리턴한다.
        # 요약하면 전체 웹툰의 넘버, 썸네일 이미지 주소, 웹툰 이름을 가진 네임드 튜플의 리스트를 반환
        # 결국엔 init 메서드에서 호출된 find_webtoon메서드를 사용하기 위해 필요한 메서드
        url = 'http://comic.naver.com/webtoon/weekday.nhn'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        webtoon_list = set()

        daily_all = soup.select_one('.list_area.daily_all')
        days = daily_all.select('div.col')
        for day in days:
            items = day.select('li')
            for item in items:
                img_url = item.select_one('div.thumb').a.img['src']
                title = item.select_one('a.title').get_text(strip=True)

                url_webtoon = item.select_one('a.title')['href']
                parse_result = urlparse(url_webtoon)
                queryset = parse_qs(parse_result.query)
                title_id = queryset['titleId'][0]

                webtoon = utils.Webtoon(title_id=title_id, img_url=img_url, title=title)
                webtoon_list.add(webtoon)

        webtoon_list = sorted(list(webtoon_list), key=lambda webtoon: webtoon.title)
        # 마지막으로 리턴된 웹툰 리스트에는 Webtoon네임드 튜플이 webtoon.title순서로 정렬됨
        return webtoon_list

    def update_episode_list(self, force_update=False):
        if force_update:
            self.episode_list = list()
        recent_episode_no = self.episode_list[0].no if self.episode_list else 0
        # 저장되어 있는 에피소드 리스트의 최종화의 no를 변수에 할당
        print('-Update episode list start (Recent episode no: %s)-'%recent_episode_no)
        page = 1
        new_list = list()
        while True:
            print('Get webtoon episode list (Loop %s)'% page)
            el = utils.get_webtoon_episode_list(self.webtoon, page)
            #1번 째 페이지의 에피소드 리스트를 el에 할당
            for episode in el: # 해당 페이지의 에피소드 리스트를 순회
                if int(episode.no) > int(recent_episode_no):
                    #utils.get_webtoon_episode_list를 통헤 가져온 최신 에피소드 no(episode.no)와
                    #기존에 가지고 있는 웹툰 리스트의 최신 no(recent_episode_no)를 비교하여
                    #최신 에피소드 리스트의 no가 더 클 경우 (True) 가장 최신화 부터 역순으로 비교한다.
                    new_list.append(episode)
                    if int(episode.no)==1:
                        break
                else:
                    break
            else:
                page += 1
                continue
            break

        self.episode_list = new_list + self.episode_list
        self.save()
        return new_list

    def get_last_page_episode_list(self):
        el = utils.get_webtoon_episode_list(self.webtoon, 99999)
        self.episode_list = el
        return len(self.episode_list)

    def print_recent_episode_num(self):
        el = utils.get_webtoon_episode_list(self.webtoon, 1)
        e = el[0]
        return(e.no)
        # print(f'{el[0].no}화 - {el[0].title}')


    def save(self, path=None):
        # 현재폴더를 기준으로 db/<webtoon_id>.txt 파일에
        # pickle로 self.episode_list를 저장
        if not os.path.isdir('db'):
            os.mkdir('db')
        obj = self.episode_list
        path = 'db/%s.txt'% self.webtoon.title_id
        pickle.dump(obj,open(path,'wb'))
        #파일 객체는 (open)은 따로 변수에 할당하지 않으면 close를 하지 안않아도 된다.(자동으로 닫힘)

    def load(self, path=None, init=False):
        try:
            path = f'db/{self.webtoon.title_id}.txt'
            self.episode_list = pickle.load(open(path,'rb'))
        except FileNotFoundError:
            if not init:
                print('파일이 없습니다.')

    def make_list_html(self):
        if not os.path.isdir("webtoon"):
            os.mkdir('webtoon')
        filename = f'webtoon/{self.webtoon.title_id}.html'
        with open(filename, 'wt') as f:
            list_html_head = open('html/list_html_head.html', 'rt').read()
            f.write(list_html_head)
            for e in self.episode_list:
                list_html_tr = open('html/list_html_tr.html','rt').read()
                f.write(list_html_tr.format(
                    img_url=f'./{self.webtoon.title_id}_thumbnail/{e.no}.jpg',
                    title=e.title,
                    rating=e.rating,
                    created_date=e.created_date
                ))
            list_html_tail = open('html/list_html_tail.html', 'rt').read()
            f.write(list_html_tail)
        return filename

    def save_all_episode_image(self):
        el = pickle.load(open(f'db/{self.webtoon.title_id}.txt', 'rb'))
        for episode_num in range(len(el)):
            e = el[episode_num]
            e._save_images()
            print(f'{e.no}화 저장 완료')

    def save_recent_episode_image(self):
        el = self.update_episode_list()
        for episode_num in range(len(el)):
            e = el[episode_num]
            e._save_images()
            print(f'{e.no}화 저장 완료')

# el = pickle.load(open('db/700843.txt', 'rb'))
# e = el[0]
# e._save_images()


# if __name__ == '__main__':
#     crawler = NaverWebtoonCrawler('유미')
#     crawler()

