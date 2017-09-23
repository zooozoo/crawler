from urllib.parse import urlparse, parse_qs
import requests
from collections import namedtuple
from bs4 import BeautifulSoup
from episode import Episode

Webtoon = namedtuple('Webtoon', ['title_id', 'img_url', 'title'])
webtoon_yumi = 651673
webtoon_p = 696617

def get_webtoon_episode_list(webtoon, page=1):
    webtoon_list_url = 'http://comic.naver.com/webtoon/list.nhn'
    params = {
        'titleId': webtoon.title_id,
        'page': page,
    }
    response = requests.get(webtoon_list_url, params=params)
    soup = BeautifulSoup(response.text, 'lxml')

    episode_list = list()
    webtoon_table = soup.select_one('table.viewList')
    tr_list = webtoon_table.find_all('tr', recursive=False)
    for tr in tr_list:
        td_list = tr.find_all('td')
        if len(td_list) < 4:
            continue
        td_thumbnail = td_list[0]
        td_title = td_list[1]
        td_rating = td_list[2]
        td_created_date = td_list[3]

        url_episode = td_thumbnail.a.get('href')
        parse_result = urlparse(url_episode)
        pqueryset = parse_qs(parse_result.query)
        no = pqueryset['no'][0]
        # 나머지 쿼리값들 중에서(키:벨류 타입으로 되어있다)
        # no 키에 해당하는 그룹으로 된 벨류의0 번째 항목(넘버번호) {no:1923}

        url_thumbnail = td_thumbnail.a.img.get('src')
        title = td_title.get_text(strip=True)
        rating = td_rating.strong.get_text(strip=True)
        created_date = td_created_date.get_text(strip=True)
        # webtoon_name = soup.select_one('div.comicinfo').div.a.img['alt']

        episode = Episode(
            webtoon=webtoon,
            no=no,
            url_thumbnail=url_thumbnail,
            title=title,
            rating=rating,
            created_date=created_date,
            # webtoon_name=webtoon_name
        )
        episode_list.append(episode)

    return episode_list
