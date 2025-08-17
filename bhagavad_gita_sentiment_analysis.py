import streamlit as st
import pandas as pd
import re

# Load your Dataset.xlsx lexicon
df = pd.read_excel('Dataset.xlsx')

def build_sentiment_dict(df, word_col='Name of Word', pos_col='Positive', neg_col='Negative'):
    sentiment_dict = {}
    for _, row in df.iterrows():
        word = str(row[word_col]).strip().lower()
        pos_score = row.get(pos_col, 0)
        neg_score = row.get(neg_col, 0)
        # Clean missing and invalid data
        if pd.isna(pos_score) or not isinstance(pos_score, (int, float)): 
            pos_score = 0
        if pd.isna(neg_score) or not isinstance(neg_score, (int, float)):
            neg_score = 0
        sentiment_dict[word] = (pos_score, neg_score)
    return sentiment_dict

# Build initial lexicon from file
sentiment_dict = build_sentiment_dict(df)

# Add or override critical Bhagavad Gita sentiment words with strong scores
custom_sentiments = {
    'anger': (0, 3),
    'delusion': (0, 2),
    'loss': (0, 2),
    'destruction': (0, 3),
    'perishes': (0, 3),
    'intelligence': (1, 0),
    'miserable': (0, 3),
    'anxious': (0, 2),
    'desire': (0, 1),
    'fear': (0, 2),
    'peace': (2, 0),
    'faith': (2, 0),
    'love': (3, 0),
    'hope': (2, 0),
    # Add more as you find needed
}

# Update lexicon with custom scores
sentiment_dict.update(custom_sentiments)

def compute_sentiment(text):
    # Tokenize text into words without nltk
    words = re.findall(r'\b\w+\b', text.lower())
    pos_total, neg_total = 0, 0
    word_details = []

    for word in words:
        pos, neg = sentiment_dict.get(word, (0, 0))
        # Ensure numeric
        if not isinstance(pos, (int, float)): pos = 0
        if not isinstance(neg, (int, float)): neg = 0
        word_details.append((word, pos, neg))
        pos_total += pos
        neg_total += neg

    if pos_total > neg_total:
        overall_sentiment = "Positive"
    elif neg_total > pos_total:
        overall_sentiment = "Negative"
    else:
        overall_sentiment = "Neutral"

    return overall_sentiment, pos_total, neg_total, word_details

st.title("Bhagavad Gita Sentiment Analysis Enhanced")

user_text = st.text_area("Enter a verse or sentence:")

if user_text:
    sentiment, total_pos, total_neg, words_scores = compute_sentiment(user_text)

    st.markdown(f"**Overall Sentiment:** {sentiment}")
    st.markdown(f"**Total Positive Score:** {total_pos}")
    st.markdown(f"**Total Negative Score:** {total_neg}")

    st.markdown("### Word-wise Sentiment Scores:")
    df_words = pd.DataFrame(words_scores, columns=['Word', 'Positive Score', 'Negative Score'])
    st.table(df_words)

    if sentiment == "Positive":
        st.success("The overall sentiment is POSITIVE.")
    elif sentiment == "Negative":
        st.error("The overall sentiment is NEGATIVE.")
    else:
        st.info("The overall sentiment is NEUTRAL.")
