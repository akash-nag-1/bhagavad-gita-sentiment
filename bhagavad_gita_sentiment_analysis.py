import streamlit as st
import pandas as pd

# Load word sentiment dictionary and data
df = pd.read_excel('Dataset.xlsx')

def build_sentiment_dict(df, word_col='Name of Word', pos_col='Positive', neg_col='Negative'):
    sentiment_dict = {}
    for _, row in df.iterrows():
        word = str(row[word_col]).strip().lower()
        pos_score = row.get(pos_col, 0)
        neg_score = row.get(neg_col, 0)
        if pd.isna(pos_score):
            pos_score = 0
        if pd.isna(neg_score):
            neg_score = 0
        sentiment_dict[word] = (pos_score, neg_score)
    return sentiment_dict

sentiment_dict = build_sentiment_dict(df)

def compute_sentiment(text):
    words = text.lower().split()
    pos_total, neg_total = 0, 0
    result_words = []
    for word in words:
        if word.isalpha():
            pos, neg = sentiment_dict.get(word, (0, 0))
            if pos != 0 or neg != 0:
                result_words.append((word, pos, neg))
            pos_total += pos
            neg_total += neg
    if pos_total > neg_total:
        sentiment = 'Positive'
    elif neg_total > pos_total:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    return sentiment, result_words, pos_total, neg_total

# Streamlit UI
st.title("Bhagavad Gita Sentiment Analysis - Lexicon Based")
user_text = st.text_area("Enter a verse or sentence:")

if user_text:
    sentiment, scored_words, pos_sum, neg_sum = compute_sentiment(user_text)
    st.write(f"**Overall Sentiment:** {sentiment}")
    st.write(f"Total Positive Score: {pos_sum}, Total Negative Score: {neg_sum}")
    st.write("**Word Details (matched in lexicon):**")
    st.table(pd.DataFrame(scored_words, columns=['Word', 'Positive', 'Negative']))
