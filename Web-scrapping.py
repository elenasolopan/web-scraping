import requests
from bs4 import BeautifulSoup

KEYWORDS = {'дизайн', 'фото', 'web', 'python'}
response = requests.get('https://habr.com/ru/all/')

if not response.ok:
    raise ValueError('No response')

text = response.text

soup = BeautifulSoup(text, features="html.parser")
articles = soup.find_all('article')

for article in articles:
    hubs = {h.text.lower() for h in article.find_all('a', class_='hub-link')}

    if KEYWORDS & hubs:
        href = article.find('a', class_="post__title_link").attrs.get('href')

        date_publish = article.find('span', class_="post__time").text

        title = article.find('a', class_="post__title_link").text

        hubs_status = True

        if not KEYWORDS & hubs:
            hubs_status = False

            title_status = False

            for tag in KEYWORDS:
                if tag in title.lower():
                    title_status = True
                    break

            if not title_status:
                previews = article.find('div', class_='post__body_crop').text
                preview_status = False

                for tag in KEYWORDS:
                    if tag in previews.lower():
                        preview_status = True
                        break

                if not hubs_status and not title_status and not preview_status:
                    continue

        print(f'<{date_publish}> - <{title}> - <{href}>')
        print()
