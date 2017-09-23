import os

import pickle
import requests
from bs4 import BeautifulSoup

from crawler2 import NaverWebtoonCrawler
from episode import Episode

el = pickle.load(open('db/700843.txt', 'rb'))
e = el[0]
print(e.title)

# os.makedirs(f'webtoon/{e.webtoon.title}/{e.webtoon.title_id}__images / {e.no}', exist_ok=True)

# self.thumbnail_dir = f'webtoon/{e.webtoon.title}/{e.webtoon.title_id}_thumbnail'
# self.image_dir = f'webtoon/{e.webtoon.title}/{e.webtoon.title}__images / {e.no}'

