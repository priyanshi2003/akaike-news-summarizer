# sample_scrap.py - For Quick News Scraping Demo

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article
from textblob import TextBlob
import nltk

nltk.download('punkt')

# --- Customize your search query here ---
query = "Tesla"  # You can change this to any topic like "Politics", "Startups", "Healthcare", etc.
site = f'https://news.google.com/rss/search?q={query}'

# --- Fetching and parsing the RSS feed ---
op = urlopen(site)
rd = op.read()
op.close()
sp_page = soup(rd, 'xml')
news_list = sp_page.find_all('item')

print(f"\nTotal Articles Found: {len(news_list)}")
print("=" * 60)

# --- Looping through articles ---
for index, news in enumerate(news_list[:10], start=1):  # Top 10 news articles
    print(f"\n📰 Article {index}")
    print("-" * 60)

    title = news.title.text
    link = news.link.text
    pub_date = news.pubDate.text

    print(f"Title       : {title}")
    print(f"Link        : {link}")
    print(f"Published At: {pub_date}")

    try:
        article = Article(link)
        article.download()
        article.parse()
        article.nlp()

        summary = article.summary
        top_image = article.top_image
        blob = TextBlob(summary)
        polarity = round(blob.sentiment.polarity, 2)
        subjectivity = round(blob.sentiment.subjectivity, 2)

        # Sentiment Label
        if polarity > 0:
            sentiment = "Positive"
        elif polarity < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        print(f"\nSummary     : {summary}")
        print(f"Sentiment   : {sentiment}")
        print(f"Polarity    : {polarity}")
        print(f"Subjectivity: {subjectivity}")
        print(f"Image Link  : {top_image}")

    except Exception as e:
        print(f"Error parsing article: {e}")

    print("=" * 60)
