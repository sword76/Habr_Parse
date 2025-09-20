import requests
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent as ua
from dataclasses import dataclass
from pprint import pprint

url = 'https://habr.com/ru/flows/backend/articles/top/daily/'

@dataclass
class ArticleData:
    title: str
    views: str
    URL: str
    text: str

def get_html(url: str) -> str:
    res = requests.get(
        url, 
        headers = {
        'User-Agent': ua().google,
        }
    )
    res.raise_for_status()
    return res.text


def get_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, 'lxml')


def get_all_habr_posts(soup: BeautifulSoup) -> list[ArticleData]:
    post_data = []
    all_articles_soup = soup.find_all('article', class_ = 'tm-articles-list__item')
    for article in all_articles_soup:
        article_title: str = article.find('a', class_ = 'tm-title__link').find('span').text
        article_url: str = article.find('a', class_ = 'tm-title__link')['href']
        article_url = 'https://habr.com' + article_url
        article_reads: str = article.find('span', class_ = 'tm-icon-counter__value').text
        article_text: str = get_article_text(article_url)
        # print(f'{article_title=}: {article_url=}, views: {article_reads}')
        post_data.append(ArticleData(
            title = article_title,
            URL = article_url,
            views = article_reads,
            text = article_text,
        ))
        time.sleep(.5)
    return post_data
    

def get_article_text(url: str) -> str:
    try:
        article_html = get_html(url)
        soup = get_soup(article_html)
        article_text = soup.find('article', class_= 'tm-article-presenter__content')
        if article_text:
            return article_text.get_text(separator='\n', strip=True)
        return "Текст статьи не найден"
    except Exception as e:
        return f"Ошибка при получении текста: {str(e)}"


def main():
    html = get_html(url)
    soup = get_soup(html)
    posts = get_all_habr_posts(soup)
    pprint(posts)


if __name__ == '__main__':
    main()