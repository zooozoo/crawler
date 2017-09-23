import requests
from bs4 import BeautifulSoup

webtoon_list_url = 'http://comic.naver.com/webtoon/list.nhn'
params = {
    'titleId': 700843,
    'page': 1,
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
    a = td_thumbnail.a.get('href')
    td_title = td_list[1]
    td_rating = td_list[2]
    td_created_date = td_list[3]

    url_thumbnail = f'http://comic.naver.com{a}'
    print(url_thumbnail)