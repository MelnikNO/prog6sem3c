from bs4 import BeautifulSoup

def parse_articles(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    selectors = [
        'h2.tm-title a.tm-title__link',
        '.tm-article-snippet__title a',
        'article .tm-title a',
        'a.tm-title__link',
        '.post__title a',
        '.tm-article-title a'
    ]
    
    title_elements = []
    for selector in selectors:
        title_elements = soup.select(selector)
        if title_elements:
            break
    
    articles = []
    for element in title_elements[:5]:
        title = element.get_text(strip=True)
        if title:
            articles.append({"title": title})
    
    if not articles:
        for heading in soup.select('h2')[:5]:
            title = heading.get_text(strip=True)
            if title and len(title) > 5:
                articles.append({"title": title})
    
    return articles
