import requests
from bs4 import BeautifulSoup

def fetch_bbc_news():
    url = 'https://www.bbc.com/news'
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('h2', {'data-testid': 'card-headline'})

    news = []
    for article in articles:
        title = article.get_text()
        link_tag = article.find_parent('a')
        if link_tag and link_tag.has_attr('href'):
            link = link_tag['href']
            if not link.startswith('http'):
                link = 'https://www.bbc.com' + link
            news.append({'title': title, 'link': link})

    return news

def save_to_html(news):
    with open("news.html", "w", encoding="utf-8") as file:
        file.write("""
        <html>
        <head>
            <title>BBC News Articles</title>
            <link rel="stylesheet" type="text/css" href="styles.css">
        </head>
        <body>
            <h1>Latest BBC News Articles</h1>
            <ul>
        """)
        for article in news:
            file.write(f"<li><a href='{article['link']}'>{article['title']}</a></li>")
        file.write("""
            </ul>
        </body>
        </html>
        """)

def main():
    news = fetch_bbc_news()
    if news:
        save_to_html(news)
        print("News articles saved to news.html")
    else:
        print("No news articles found.")

if __name__ == '__main__':
    main()
