import os
from urllib.parse import urlencode

import pickle
import requests
from bs4 import BeautifulSoup

class Episode:
    # Episode클래스는 각 웹툰별로 사용하는 클래스
    def __init__(self, webtoon, no, url_thumbnail, title, rating, created_date):
        self._webtoon = webtoon
        self._no = no
        self._url_thumbnail = url_thumbnail
        self._title = title
        self._rating = rating
        self._created_date = created_date

        self.thumbnail_dir = f'webtoon/{self.webtoon.title}/{self.webtoon.title_id}_thumbnail'
        # self.image_dir = f'webtoon/{self.webtoon.title}/{self.webtoon.title_id}__images / {self.no}'
        self.save_thumbnail()

    # {self.webtoon.title}_images / {self.no}

    @property
    def webtoon(self):
        return self._webtoon

    @property
    def no(self):
        return self._no

    @property
    def url_thumbnail(self):
        return self._url_thumbnail

    @property
    def title(self):
        return self._title

    @property
    def rating(self):
        return self._rating

    @property
    def created_date(self):
        return self._created_date

    @property
    def has_thumbnail(self):
        path = f'{self.thumbnail_dir}/{self.no}.jpg'
        return os.path.exists(path)

    def save_thumbnail(self, force_update=True):
        if not self.has_thumbnail or force_update:
            os.makedirs(self.thumbnail_dir, exist_ok=True)
            response = requests.get(self._url_thumbnail)
            filepath = f'{self.thumbnail_dir}/{self.no}.jpg'
            if not os.path.exists(filepath):
                with open(filepath, 'wb') as f:
                    f.write(response.content)

    def _save_images(self):
        # path = self.image_dir
        # check_file_exists = os.path.exists(path)
        # if not check_file_exists:
        #     os.makedirs(path, exist_ok=True)

        os.makedirs(f'webtoon/{self.webtoon.title}/{self.webtoon.title_id}_images/{self.no}_{self.title}', exist_ok=True)
        params = {
            'titleId': self.webtoon.title_id,
            'no': self.no
        }
        url_contents = 'http://comic.naver.com/webtoon/detail.nhn?'+ urlencode(params)
        response = requests.get(url_contents)
        soup = BeautifulSoup(response.text, 'lxml')
        img_list = soup.select_one('.wt_viewer').find_all('img')
        url_img_list = [img['src'] for img in img_list]

        for index, url in enumerate(url_img_list):
            headers = {
                'Referer': url_contents
            }
            response = requests.get(url, headers=headers)
            with open(f'webtoon/{self.webtoon.title}/{self.webtoon.title_id}_images/{self.no}_{self.title}/{index +1}.jpg', 'wb') as f:
                f.write(response.content)




if __name__ == '__main__':
    # el = pickle.load(open('db/700843.txt', 'rb'))
    # e = el[0]
    e._save_all_episode_image()