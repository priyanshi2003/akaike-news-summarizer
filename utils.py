# utils.py

import requests
from textblob import TextBlob
from googletrans import Translator
from gtts import gTTS
from datetime import datetime
import base64

API_KEY = '26d5afbc5bdf4c598cbcf4ac2bbab9a3'
DEFAULT_IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiSZNX30yLNN4mHncrJTKWwnG4mJE7Sk-ovYNx9_BLLsr3LGON6lSozAg&s"
translator = Translator()

def fetch_articles(query):
    url = f'https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data.get("articles", [])

def sort_articles_by_date(articles):
    for article in articles:
        try:
            article["publishedAt_dt"] = datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
        except:
            article["publishedAt_dt"] = datetime.min
    return sorted(articles, key=lambda x: x["publishedAt_dt"], reverse=True)

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = round(blob.sentiment.polarity, 2)
    subjectivity = round(blob.sentiment.subjectivity, 2)
    sentiment_label = "😐 Neutral"
    if polarity > 0:
        sentiment_label = "😊 Positive"
    elif polarity < 0:
        sentiment_label = "☹️ Negative"
    return sentiment_label, polarity, subjectivity

def translate_to_hindi(text):
    try:
        translated = translator.translate(text, dest='hi')
        return translated.text
    except Exception:
        return "Translation failed."

def generate_audio(text, filename):
    try:
        tts = gTTS(text=text, lang='hi')
        tts.save(filename)
        return filename
    except:
        return None

def encode_audio_base64(filepath):
    try:
        with open(filepath, "rb") as audio_file:
            audio_bytes = audio_file.read()
            return base64.b64encode(audio_bytes).decode()
    except:
        return None
