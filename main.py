import requests
import bs4
from progress.bar import Bar

url = 'https://habr.com'

HUBS = [
    'Python *',
    'python'
    'Игры и игровые консоли, '
    'DIY'
    'дизайн',
    'фото',
    'web',
]

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}


def research_by_hubs(articles_preview):
    for article in articles_preview:
        hubs = article.find_all(class_='tm-article-snippet__hubs-item')
        hubs = [hub.text.strip() for hub in hubs]
        for hub in hubs:
            if hub in HUBS:
                href = article.find(class_='tm-article-snippet__title-link').attrs['href']
                title = article.find('h2').find('span').text
                date = article.find(class_='tm-article-snippet__datetime-published').find('time').text
                print(f'{date} {title} ===> {url}{href}')


def research_by_text(articles_full_text):
    article_reference = []
    progress_bar = Bar('Processing', max=len(articles_full_text), suffix='%(percent)d%%')
    for article in articles_full_text:
        href = article.find(class_='tm-article-snippet__title-link').attrs['href']
        full_link = url + href
        response_article = requests.get(full_link, headers=HEADERS)
        text_new_link = response_article.text
        soup_new_link = bs4.BeautifulSoup(text_new_link, features='html.parser')
        article_new_link = soup_new_link.find(id='post-content-body').find_all('p')
        progress_bar.next()
        for text_case in article_new_link:
            text_standard = text_case.text.lower()
            for hub in HUBS:
                hub_standard = hub.lower()
                if hub_standard in text_standard:
                    title = article.find('h2').find('span').text
                    date = article.find(class_='tm-article-snippet__datetime-published').find('time').text
                    example = f'\nНашел упоминания в "{title}" от "{date}" ===> {url}{href}'
                    if example not in article_reference:
                        article_reference.append(example)
    for correct_article in article_reference:
        print(correct_article)


if __name__ == '__main__':
    response = requests.get(url, headers=HEADERS)
    text = response.text
    soup = bs4.BeautifulSoup(text, features='html.parser')
    articles = soup.find_all('article')
    while True:
        print('Выберите нужное\n 1) Искать статьи по тегам\n 2) Искать статьи по упоминаниям тегов\n 3) Выйти')
        user_answer = input('Ваш ответ: ')
        if user_answer == '1':
            research_by_hubs(articles)
        elif user_answer == '2':
            research_by_text(articles)
        elif user_answer == '3':
            print('Возвращайтесь!')
            break
        else:
            print('Такой команды нет, повторите попытку')
