import os

import pickle
import requests
from bs4 import BeautifulSoup

from crawler2 import NaverWebtoonCrawler
from episode import Episode

# el = pickle.load(open('db/700843.txt', 'rb'))
# e = el[0]
# print(len(el))

# os.makedirs(f'webtoon/{e.webtoon.title}/{e.webtoon.title_id}__images / {e.no}', exist_ok=True)

# self.thumbnail_dir = f'webtoon/{e.webtoon.title}/{e.webtoon.title_id}_thumbnail'
# self.image_dir = f'webtoon/{e.webtoon.title}/{e.webtoon.title}__images / {e.no}'
# while True:
choice = input('1, 2, 3 중에 선택')
if choice == 1:
    print('1번 선택')
    # break
elif choice == 2:
    print('2번 선택')
    # break
else:
    print('3번 선택')
    # break