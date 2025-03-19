# 📰 Akaike - Smart News Summarizer

Akaike - Smart News Summarizer is an advanced NLP-powered application built using Streamlit that allows users to fetch, summarize, analyze, and listen to the latest news articles in both English and Hindi (TTS). It is an all-in-one news exploration and sentiment analysis tool that visually and audibly enhances user experience.

---

## 🚀 Implementation Overview

The application is implemented using Python and the Streamlit framework, powered by:
- **NewsAPI** for fetching recent and relevant news articles.
- **TextBlob** for sentiment analysis (polarity, subjectivity).
- **Googletrans** for translating summaries into Hindi.
- **gTTS (Google Text-to-Speech)** for generating audio in Hindi.
- **Scikit-learn (CountVectorizer)** for topic extraction and overlap analysis.
- **Matplotlib and WordCloud** for visualizations (pie chart and word cloud).

### 📋 Key Functionalities:
- Topic selection: Trending, Favorite, or Custom Query
- News summarization per article
- Sentiment & subjectivity analysis with score
- Hindi audio summary for each article
- Keyword-based topic detection per article
- Word cloud visualization
- Pie chart for sentiment distribution
- Comparative analysis summary with final Hindi audio

---

## 📦 Project Structure
```
├── App.py                    # Main Streamlit application
├── utils.py                 # Utility functions (API calls, sentiment, audio)
├── api.py                   # (Optional) Modular API file for extensibility
├── requirements.txt         # All required dependencies
├── news 2.jpg               # Welcome image on app load
└── README.md                # Documentation
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
https://huggingface.co/spaces/your-username/your-space-name
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate       # For Linux/macOS
.venv\Scripts\activate         # For Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Add Your NewsAPI Key
Open `utils.py` and replace the placeholder:
```python
API_KEY = 'your_api_key_here'
```

---

## ▶️ How to Run Locally
```bash
streamlit run App.py
```

The application will run in your browser at `http://localhost:8501`

---

## 🗂 Dependencies (requirements.txt)
```
streamlit
matplotlib
textblob
gtts
googletrans==4.0.0rc1
scikit-learn
wordcloud
requests
```

---

## ✅ Deployment on Hugging Face Spaces
1. Create a new Space at https://huggingface.co/spaces
2. Choose **"Streamlit"** as the SDK
3. Upload all required files: `App.py`, `utils.py`, `requirements.txt`, and image
4. Hugging Face will auto-deploy the app
5. Share your space URL (example: https://huggingface.co/spaces/username/akaike-news)

---

## 💡 Notes:
- Avoid using emoji characters in label titles to avoid Unicode issues.
- Keep the TTS files small for faster load on web.

---

## ✍️ Conclusion
This project demonstrates the power of integrating NLP, sentiment analytics, and TTS in a news-based application. It’s scalable and can be enhanced further with REST APIs, databases, or multi-language support.



---

📧 For queries, contact: priyanshi24b@gim.ac.in


