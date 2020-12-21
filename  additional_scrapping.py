import requests
from bs4 import BeautifulSoup
import datetime
import pprint

# Определяем список ключевых слов
KEYWORDS = ['привет', 'атака', 'объектно-ориентированное программирование', 'darpa', 'китай']

# Получаем дату
now = datetime.datetime.now()
today = datetime.datetime.date(now)


def get_article_by_fulltext(url, keywords):
    # Заходим на сайт и ищем по всем статьям
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_posts = soup.find_all('article', class_='post post_preview')
    result = []
    # Получаем ссылку конкретной статьи
    for post in all_posts:
        full_article = post.find_all('div', class_='post__body post__body_crop')
        preview_text = list(map(lambda x: x.text.strip().lower(), full_article))
        for text in preview_text:
            link = post.find('a', class_='post__title_link')
            link_link = link.attrs.get('href')
            # Переходим по ссылке статьи
            article_response = requests.get(link_link)
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
            full_text_posts = article_soup.find_all('div', class_='post__text post__text-html post__text_v1')
            # Берем весь текст который есть и в нем находим текст статьи
            for text in full_text_posts:
                for words in text:
                    # Если в тексте есть совпадения то добавляем дату, титул и ссылку на конкретную статью в список
                    if any((x in words for x in keywords)):
                        dt = post.find('span', class_='post__time').text.strip()
                        if 'сегодня' in dt:
                            dt = f'Дата: {today.day}.{today.month}.{today.year}'
                        link = post.find('a', class_='post__title_link')
                        link_link = link.attrs.get('href')
                        link_text = link.text.strip()
                        result.append([dt, link_text, link_link])
                        print([dt, link_text, link_link])
                        break
    return result


if __name__ == '__main__':
    my_articles = get_article_by_fulltext('https://habr.com/ru/all/', KEYWORDS)
