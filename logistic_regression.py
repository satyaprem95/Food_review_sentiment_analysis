import streamlit as st
import numpy as np
import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from translate import Translator

# Load the trained model
def load_model(model_path):
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

# Load the vectorizer
def load_vectorizer(vectorizer_path):
    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)
    return vectorizer

languages = {
    'English': 'en',
    'Gujarati': 'gu-IN',
    'Hindi': 'hi-IN',
    'Kannada': 'kn-IN',
    'Konkani': 'kok',
    'Marathi': 'mr-IN',
    'Punjabi': 'pa-IN',
    'Sanskrit': 'sa-IN',
    'Tamil': 'ta-IN',
    'Telugu': 'te-IN'
}

st.title('Multilingual Comment Analyzer')

# Load model and vectorizer
lmodel = load_model('logistic_regression_model.pkl')
vectorizer = load_vectorizer('tfidf_vectorizer.pkl')

# User input
st.subheader('Enter Sentence')
new_sentence = st.text_input('Enter a sentence:')

st.subheader('Translate to Language')
convert_lang = st.selectbox('Select language:', list(languages.keys()))

if new_sentence:
    translator = Translator(from_lang='en', to_lang=languages[convert_lang])
    translation = translator.translate(new_sentence)
    st.write('Translated Sentence:', translation)

    # Sentiment analysis
    st.subheader('Sentiment Analysis')

    # Vectorize the preprocessed sentence
    X_new = vectorizer.transform([new_sentence])
    
    # Predict sentiment
    predicted_sentiment = lmodel.predict(X_new)

    # Display sentiment
    sentiment = "Positive" if predicted_sentiment[0] == 1 else "Negative"
    st.write('Predicted Sentiment:', sentiment)
