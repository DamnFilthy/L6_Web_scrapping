import requests
from bs4 import BeautifulSoup
import datetime

now = datetime.datetime.now()
today = datetime.datetime.date(now)
response = requests.get('https://2ip.ru/')

soup = BeautifulSoup(response.text, 'html.parser')
el = soup.find(id="d_clip_button")
print(el.text.strip())

index_id = response.text.index('id="d_clip_button"')
index_span_start = response.text.index('<span>', index_id)
index_span_end = response.text.index('</span>', index_span_start)

print(response.text[index_span_start + 6: index_span_end])

DESIRED_HUBS = ['программирование', 'android', 'agile', 'фото']
response_habr = requests.get('https://habr.com/ru/all/')
soup_habr = BeautifulSoup(response_habr.text, 'html.parser')

# posts = soup_habr.find_all('article', class_='post')
# for post in posts:
#     hubs = post.find_all('li', class_='inline-list__item_hub')
#     hubs_text = list(map(lambda x: x.text.strip().lower(), hubs))
#     # hub_text = []
#     # for hub in hubs:
#     #     hub_text.append(hub.text.strip())
#     for hub_text in hubs_text:
#         if any((x in hub_text for x in DESIRED_HUBS)):
#             dt = post.find('span', class_='post__time').text.strip()
#             if 'сегодня' in dt:
#                 dt = today
#             link = post.find('a', class_='post__title_link')
#             link_link = link.attrs.get('href')
#             link_text = link.text.strip()
#             print(dt, link_text, link_link)
#             break
