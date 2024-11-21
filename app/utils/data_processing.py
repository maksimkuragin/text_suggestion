import pandas as pd
import re
import nltk
from nltk.corpus import words

nltk.download('words', quiet=True)
word_list = set(words.words())

def clean_message(msg):
    msg = re.sub(r'[^\w\s]', '', msg)
    tokens = msg.lower().split()
    filtered_words = [word for word in tokens if word in word_list]
    return filtered_words

def load_and_clean_data():
    emails = pd.read_csv('data/emails_100.csv')
    emails['cleaned_message'] = emails['message'].apply(clean_message)
    corpus = emails['cleaned_message'].tolist()
    return corpus
