import os

import pickle
import requests
from bs4 import BeautifulSoup

from crawler2 import NaverWebtoonCrawler
from episode import Episode

#디렉토리 안의 파일의 갯수 구하기
el = pickle.load(open('db/700843.txt', 'rb'))
e = el[0]
path= f'webtoon/{e.webtoon.title}/{e.webtoon.title_id}__images / {e.no}_{e.title}' #image file root
img_file_number = os.listdir(path)
print(len(a))


# os.makedirs(f'webtoon/{e.webtoon.title}/{e.webtoon.title_id}__images / {e.no}', exist_ok=True)

# self.thumbnail_dir = f'webtoon/{e.webtoon.title}/{e.webtoon.title_id}_thumbnail'
# self.image_dir = f'webtoon/{e.webtoon.title}/{e.webtoon.title}__images / {e.no}'
# while True:

