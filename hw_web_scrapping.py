import requests
from bs4 import BeautifulSoup
import datetime
import pprint

# Определяем список ключевых слов
KEYWORDS = ['привет', 'атака', 'объектно-ориентированное программирование', 'darpa', 'китай']

# Получаем дату
now = datetime.datetime.now()
today = datetime.datetime.date(now)


def get_articles_by_preview(url, keywords):
    # Делаем запрос к статьям на сайте ЦЕЛИКОМ
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_posts = soup.find_all('article', class_='post post_preview')
    # Будем возвращать список с нужными нам статьями
    result = []
    for post in all_posts:
        # Находим превью статей и в них уже ищем ключевые слова
        preview = post.find_all('div', class_='post__body post__body_crop')
        preview_text = list(map(lambda x: x.text.strip().lower(), preview))
        for text in preview_text:
            if any((x in text for x in keywords)):
                # если в тексте превью есть совпадения, то мы берем дату, титул и ссылку этой статьи
                # которые по разметке находятся выше превью (для этого мы и брали все статьи со страницы целиком)
                dt = post.find('span', class_='post__time').text.strip()
                if 'сегодня' in dt:
                    # Если передавать дату просто как dt = today, то будет кортеж
                    # специально формируем красивую строку
                    dt = f'Дата: {today.day}.{today.month}.{today.year}'
                link = post.find('a', class_='post__title_link')
                link_link = link.attrs.get('href')
                link_text = link.text.strip()
                result.append([dt, link_text, link_link])
                print([dt, link_text, link_link])
    return result


if __name__ == '__main__':
    searched_articles = get_articles_by_preview('https://habr.com/ru/all/', KEYWORDS)
