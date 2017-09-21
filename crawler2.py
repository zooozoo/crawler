import os
import pickle

import utils


class NaverWebtoonCrawler:
    def __init__(self, webtoon_id,):
        self.webtoon_id = webtoon_id
        self.episode_list = list()
        self.load(init=True)

    def total_episode_count(self):
        el = utils.get_webtoon_episode_list(self.webtoon_id)

    # webtoon_id에 해당하는 실제 웹툰의 총 episode
    @property
    def get_total_episode_count(self):
        el = utils.get_webtoon_episode_list(self.webtoon_id)
        return int(el[0].no)

    @property
    def up_to_date(self):
        cur_episode_count = len(self.episode_list)
        total_episode_count = self.get_total_episode_count
        return cur_episode_count == total_episode_count


    def update_episode_list(self, force_update=False):
        recent_episode_no = self.episode_list[0].no if self.episode_list else 1
        # 저장되어 있는 에피소드 리스트의 최종화의 no를 변수에 할당
        print('-Update eoisode list start (Recent episode no: %s)-'%recent_episode_no)
        page = 1
        new_list = []
        while True:
            print( 'Get webtoon episode list (Loop %s)'% page)
            el = utils.get_webtoon_episode_list(self.webtoon_id, page)
            #1번 째 페이지의 에피소드 리스트를 el에 할당
            for episode in el: # 해당 페이지의 에피소드 리스트를 순회
                if int(episode.no) > int(recent_episode_no):
                    #가지고 있는 웹툰 리스트의 최신 no와 기존의 에피소드 no를 비교하여 최신 에피소드 리스트의 no가 더 클 경우 True
                    new_list.append(episode)
                    if int(episode.no) ==1:
                        break
                else:
                    break
            else:
                page += 1
                continue
            break

        self.episode_list = new_list + self.episode_list
        return len(new_list)

    def get_last_page_episode_list(self):
        el = utils.get_webtoon_episode_list(self.webtoon_id, 99999)
        self.episode_list = el
        return len(self.episode_list)


    def save(self, path=None):
        if not os.path.isdir('db'):
            os.mkdir('db')
        obj = self.episode_list
        path = 'db/%s.txt'% self.webtoon_id
        pickle.dump(obj,open(path,'wb'))
        #파일 객체는 (open)은 따로 변수에 할당하지 않으면 close를 하지 안않아도 된다.(자동으로 닫힘)

    def load(self, pathe=None, init=False):
        try:
            path = f'db/{self.webtoon_id}.txt'
            self.episode_list =pickle.load(open(path,'rb'))
        except FileNotFoundError:
            if not init:
                print('파일이 없습니다.')


# nwc=NaverWebtoonCrawler(696617)
# print(nwc.load())
