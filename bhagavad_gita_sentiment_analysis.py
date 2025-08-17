import streamlit as st
import pandas as pd
import nltk

# Ensure nltk 'punkt' tokenizer is downloaded (with check to avoid errors on Streamlit Cloud)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Load your Dataset.xlsx containing sentiment lexicon
df = pd.read_excel('Dataset.xlsx')

def build_sentiment_dict(df, word_col='Name of Word', pos_col='Positive', neg_col='Negative'):
    sentiment_dict = {}
    for _, row in df.iterrows():
        word = str(row[word_col]).strip().lower()
        pos_score = row.get(pos_col, 0)
        neg_score = row.get(neg_col, 0)
        if pd.isna(pos_score): pos_score = 0
        if pd.isna(neg_score): neg_score = 0
        if not isinstance(pos_score, (int, float)): pos_score = 0
        if not isinstance(neg_score, (int, float)): neg_score = 0
        sentiment_dict[word] = (pos_score, neg_score)
    return sentiment_dict

sentiment_dict = build_sentiment_dict(df)

def compute_sentiment_all_words(text):
    words = nltk.word_tokenize(text.lower())
    results = []
    pos_total, neg_total = 0, 0
    for word in words:
        if word.isalpha():
            pos, neg = sentiment_dict.get(word, (0, 0))
            if not isinstance(pos, (int, float)): pos = 0
            if not isinstance(neg, (int, float)): neg = 0
            results.append((word, pos, neg))
            pos_total += pos
            neg_total += neg
        else:
            # Include punctuation or non-alpha with 0 scores if needed
            results.append((word, 0, 0))
    if pos_total > neg_total:
        overall_sentiment = "Positive"
    elif neg_total > pos_total:
        overall_sentiment = "Negative"
    else:
        overall_sentiment = "Neutral"
    return overall_sentiment, pos_total, neg_total, results

st.title("Bhagavad Gita Sentiment Analysis - Detailed Lexicon View")
user_text = st.text_area("Enter a verse or sentence:")

if user_text:
    overall_sentiment, pos_sum, neg_sum, word_scores = compute_sentiment_all_words(user_text)

    st.markdown(f"**Overall Sentiment:** {overall_sentiment}")
    st.markdown(f"**Total Positive Score:** {pos_sum}")
    st.markdown(f"**Total Negative Score:** {neg_sum}")

    st.markdown("### Word Details (all words including unmatched):")
    df_words = pd.DataFrame(word_scores, columns=['Word', 'Positive', 'Negative'])
    st.table(df_words)

    # Additional: Show summary message
    if overall_sentiment == "Positive":
        st.success("The overall sentiment of the verse is POSITIVE.")
    elif overall_sentiment == "Negative":
        st.error("The overall sentiment of the verse is NEGATIVE.")
    else:
        st.info("The overall sentiment of the verse is NEUTRAL.")
