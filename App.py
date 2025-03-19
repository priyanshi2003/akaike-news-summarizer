import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
from wordcloud import WordCloud
from utils import (
    fetch_articles, sort_articles_by_date, analyze_sentiment,
    translate_to_hindi, generate_audio, encode_audio_base64, DEFAULT_IMAGE_URL
)

# Welcome image path
WELCOME_IMAGE_URL = "news 2.jpg"

# Page configuration
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: white;'>📰 Akaike - Smart News Summarizer </h1>", unsafe_allow_html=True)

# Container for right-side content
main_col2 = st.container()

# --- Sidebar Input Section ---
with st.sidebar:
    st.markdown("### 🧾 Select Input Options")

    # Dropdown for topic category
    category = st.selectbox("Choose News Category:", ["Trending Topics", "Favorite Topics", "None"])

    # Topic selection based on chosen category
    topic = None
    if category == "Trending Topics":
        topic = st.selectbox("Select a Trending Topic:", ["AI", "Climate", "Healthcare", "Sports", "Fashion", "None"])
    elif category == "Favorite Topics":
        topic = st.selectbox("Select a Favorite Topic:", ["Technology", "Startups", "None"])

    # Optional company name and user-defined query
    company = st.text_input("Or enter a Company Name (Optional):")
    user_query = st.text_input("Ask any Random Query:")
    fetch_news = st.button("\U0001F50D Fetch News")  # Search icon button

# --- Main Content Section ---
with main_col2:
    # Display welcome image when app loads
    if not fetch_news:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(WELCOME_IMAGE_URL, caption="Welcome to Akaike Smart News Summarizer", use_container_width=True)

    # If user clicks Fetch News
    if fetch_news:
        query = user_query or topic or company

        if query and query != "None":
            articles = fetch_articles(query)
            articles = sort_articles_by_date(articles)

            if not articles:
                st.warning("\u274C No articles found. Try another query.")
            else:
                st.markdown(f"### ✅ Total Articles Found: {len(articles)}")
                st.markdown("<hr>", unsafe_allow_html=True)

                sentiment_counts = {"\U0001F60A Positive": 0, "\u2639\ufe0f Negative": 0, "\U0001F610 Neutral": 0}
                all_summaries = []
                article_topics = []

                # --- Process Articles ---
                for article in articles[:10]:
                    summary = article.get("description") or "No summary available."
                    sentiment_label, polarity, subjectivity = analyze_sentiment(summary)
                    sentiment_counts[sentiment_label] += 1
                    all_summaries.append(summary)

                    # Extract keywords for topic overlap
                    vectorizer = CountVectorizer(stop_words='english')
                    vec = vectorizer.fit_transform([summary])
                    keywords = vectorizer.get_feature_names_out()
                    article_topics.append(", ".join(keywords[:5]) if keywords.any() else "No Topics Found")

                # --- Word Cloud Visualization ---
                st.subheader("\u2601\ufe0f Keyword Word Cloud")
                wordcloud = WordCloud(width=500, height=200, background_color='black', colormap='Set2').generate(" ".join(all_summaries))
                fig_wc, ax_wc = plt.subplots()
                ax_wc.imshow(wordcloud, interpolation='bilinear')
                ax_wc.axis('off')
                st.pyplot(fig_wc)

                # --- Topic Overlap Analysis ---
                st.subheader("\U0001F9E0 Topic Overlap / Keyword Analysis")
                vectorizer = CountVectorizer(stop_words='english')
                X = vectorizer.fit_transform(all_summaries)
                keywords = vectorizer.get_feature_names_out()
                keyword_freq = dict(zip(keywords, X.toarray().sum(axis=0)))
                sorted_keywords = dict(sorted(keyword_freq.items(), key=lambda item: item[1], reverse=True))

                top_keywords = list(sorted_keywords.keys())[:10]
                st.markdown("**Top Overlapping Keywords Across Articles:**")
                st.markdown(", ".join(top_keywords))

                # --- News Articles Expander ---
                with st.expander("Click to View News Articles in Detail"):
                    article_details = []

                    for i, article in enumerate(articles[:10]):
                        with st.container():
                            title = article.get("title", "No Title")
                            article_details.append({
                                "title": title,
                                "summary": summary,
                                "sentiment": sentiment_label
                            })

                            image_url = article.get("urlToImage") or DEFAULT_IMAGE_URL
                            published_at = article.get("publishedAt")
                            summary = article.get("description") or "No summary available."
                            source = article.get("source", {}).get("name", "Unknown")
                            url = article.get("url", "")
                            topics = article_topics[i]

                            sentiment_label, polarity, subjectivity = analyze_sentiment(summary)

                            st.markdown(f"<h4 style='color:lightblue'>\U0001F4F0 Article {i+1}</h4>", unsafe_allow_html=True)
                            st.image(image_url, width=250)

                            if published_at:
                                try:
                                    date_obj = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ')
                                    formatted_date = date_obj.strftime('%B %d, %Y %I:%M %p')
                                    st.markdown(f"<p style='color:lightgreen'>\u23F0 {formatted_date}</p>", unsafe_allow_html=True)
                                except:
                                    pass

                            st.markdown(f"**Title:** {title}")
                            st.markdown(f"**Summary:** {summary}")
                            st.markdown(f"**Sentiment:** {sentiment_label}")
                            if polarity != 0.0:
                                st.markdown(f"**Polarity Score:** {polarity}")
                            if subjectivity != 0.0:
                                st.markdown(f"**Subjectivity Score:** {subjectivity}")
                            st.markdown(f"**Topics:** {topics}")
                            st.markdown(f"**Source:** {source} | [Read Article]({url})")
                            st.progress((polarity + 1) / 2)

                            # Hindi Audio for Article Summary
                            hindi_summary = translate_to_hindi(summary)
                            filename = generate_audio(hindi_summary, f"summary_hi_{i}.mp3")
                            b64 = encode_audio_base64(filename)
                            audio_html = f"<audio controls preload='none'><source src='data:audio/mp3;base64,{b64}' type='audio/mp3'></audio>" if b64 else "<i>Hindi Audio Not Available</i>"
                            st.markdown(audio_html, unsafe_allow_html=True)

                # --- Sentiment Distribution Pie Chart ---
                st.subheader("\U0001F4CA Sentiment Distribution Summary")
                labels = list(sentiment_counts.keys())
                values = list(sentiment_counts.values())
                colors = ['#205781', '#4F959D', '#98D2C0']

                def autopct_format(pct):
                    return f'{pct:.1f}%' if pct > 0 else ''

                fig, ax = plt.subplots(figsize=(2.2, 2.2), dpi=150, facecolor='none')
                wedges, texts, autotexts = ax.pie(
                    values,
                    labels=None,
                    autopct=autopct_format,
                    startangle=90,
                    colors=colors,
                    textprops={'color': 'white', 'fontsize': 6}
                )
                ax.axis('equal')
                ax.legend(wedges, labels, title="Sentiments", loc="center left", bbox_to_anchor=(1, 0.5), frameon=False, fontsize=6, title_fontsize=7, labelcolor='white')
                plt.setp(autotexts, size=6, weight="regular")
                st.pyplot(fig, clear_figure=True, bbox_inches='tight', pad_inches=0.1)

                # --- Comparative Summary ---
                # 📋 Comparative Analysis Section (Only Sentiment & Summary Comparison)
                from difflib import SequenceMatcher

                # Article-wise Comparative Analysis Section
                st.markdown("### 📋 Article-wise Comparative Analysis")



                def generate_comparative_analysis(articles_data):
                    comparisons = []
                    n = len(articles_data)

                    for i in range(n):
                        for j in range(i + 1, n):
                            a1 = articles_data[i]
                            a2 = articles_data[j]

                            title1 = a1["title"]
                            title2 = a2["title"]

                            # Sentiment difference
                            sentiment_diff = ""
                            if a1["sentiment"] != a2["sentiment"]:
                                sentiment_diff = f"Article **'{title1}'** has a **{a1['sentiment']}** sentiment, while **'{title2}'** has a **{a2['sentiment']}** sentiment."

                            # Summary similarity
                            sim = SequenceMatcher(None, a1["summary"], a2["summary"]).ratio()
                            if sim < 0.6:
                                summary_diff = "The articles present distinct viewpoints or focus areas."
                            else:
                                summary_diff = "The articles seem to present similar perspectives or themes."

                            # Add only meaningful comparisons
                            if sentiment_diff or sim < 0.6:
                                comparisons.append({
                                    "Article Pair": f"{title1} ↔ {title2}",
                                    "Sentiment Comparison": sentiment_diff,
                                    "Summary Similarity Score": f"{round(sim * 100, 2)}%",
                                    "Summary Insight": summary_diff
                                })

                    return comparisons[:6]  # Return top 6


                comparison_results = generate_comparative_analysis(article_details)

                for idx, comp in enumerate(comparison_results):
                    st.markdown(f"#### 🔸 Comparison {idx + 1}: {comp['Article Pair']}")
                    if comp["Sentiment Comparison"]:
                        st.markdown(f"- 🧠 **Sentiment Insight:** {comp['Sentiment Comparison']}")
                    st.markdown(f"- 📚 **Summary Similarity Score:** {comp['Summary Similarity Score']}")
                    st.markdown(f"- 📎 **Summary Comparison:** {comp['Summary Insight']}")
                    st.markdown("---")

                # --- Final Audio Summary ---
                # Final Hindi Audio Summary
                comp_summary_text = "Here is the summary of article-wise comparisons:\n\n"
                for comp in comparison_results[:6]:
                    if comp["Sentiment Comparison"]:
                        comp_summary_text += f"{comp['Sentiment Comparison']}\n"
                    comp_summary_text += f"{comp['Summary Insight']}\n\n"

                hindi_final = translate_to_hindi(comp_summary_text)
                final_audio = generate_audio(hindi_final, "final_summary_hi.mp3")
                final_b64 = encode_audio_base64(final_audio)
                final_audio_html = f"<audio controls preload='none'><source src='data:audio/mp3;base64,{final_b64}' type='audio/mp3'></audio>" if final_b64 else "<i>Hindi Audio Not Available</i>"
                st.markdown(final_audio_html, unsafe_allow_html=True)


        else:
            st.warning(" Please enter a query or select a topic/company.")
