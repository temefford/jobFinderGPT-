
from io import StringIO

# Scikit-learn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF
from sklearn.metrics import f1_score, accuracy_score

# nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

# Utility
import string
import re
import numpy as np
import os
from collections import Counter
import logging
import time
import pickle
import itertools
import random
import datetime

# Warnings
import warnings
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')

# read file


def return_jobs(string_data, json_list):

    # ML code here
    # DataFrame
    df = pd.DataFrame(json_list)
    mdf = pd.DataFrame()
    mdf['text'] = (df['job_title'] + ' ' + df['company_name']
                + ' ' + df['job_location']).copy()
    mdf['job_url'] = df['job_url'].copy()

    stop_words = set(stopwords.words("english"))
    stop_words.remove('not')
    more_stopwords = {'one', 'br', 'Po', 'th', 'sayi', 'fo', 'Unknown'}
    stop_words = stop_words.union(more_stopwords)

    stemmer = SnowballStemmer("english")

    def remove_URL(text):
        url = re.compile(r'https?://\S+|www\.\S+')
        return url.sub(r'', text)

    def remove_emoji(text):
        emoji_pattern = re.compile(
            '['
            u'\U0001F600-\U0001F64F'  # emoticons
            u'\U0001F300-\U0001F5FF'  # symbols & pictographs
            u'\U0001F680-\U0001F6FF'  # transport & map symbols
            u'\U0001F1E0-\U0001F1FF'  # flags (iOS)
            u'\U00002702-\U000027B0'
            u'\U000024C2-\U0001F251'
            ']+',
            flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)

    def remove_html(text):
        html = re.compile(r'^[^ ]<.*?>|&([a-z0-9]+|#[0-9]\"\'\“{1,6}'
                          r'|#x[0-9a-f]{1,6});[^A-Za-z0-9]+')
        return re.sub(html, '', text)

    def remove_punct(text):
        table = str.maketrans('', '', string.punctuation)
        return text.translate(table)

    def remove_quotes(text):
        quotes = re.compile(r'[^A-Za-z0-9\s]+')
        return re.sub(quotes, '', text)

    mdf['mod_text'] = mdf['text'].apply(lambda x: remove_URL(x))
    mdf['mod_text'] = mdf['mod_text'].apply(lambda x: remove_emoji(x))
    mdf['mod_text'] = mdf['mod_text'].apply(lambda x: remove_html(x))
    mdf['mod_text'] = mdf['mod_text'].apply(lambda x: remove_punct(x))
    mdf['mod_text'] = mdf['mod_text'].apply(lambda x: remove_quotes(x))

    mdf['tokenized'] = mdf['mod_text'].apply(word_tokenize)

    mdf['lower'] = mdf['tokenized'].apply(
        lambda x: [word.lower() for word in x])

    mdf['stopwords_removed'] = mdf['lower'].apply(
        lambda x: [word for word in x if word not in stop_words])

    mdf['pos_tags'] = mdf['stopwords_removed'].apply(nltk.tag.pos_tag)

    def get_wordnet_pos(tag):
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('N'):
            return wordnet.NOUN
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    mdf['wordnet_pos'] = mdf['pos_tags'].apply(
        lambda x: [(word, get_wordnet_pos(pos_tag)) for (word, pos_tag) in x])

    wnl = WordNetLemmatizer()

    mdf['lemmatized'] = mdf['wordnet_pos'].apply(
        lambda x: [wnl.lemmatize(word, tag) for word, tag in x])

    mdf['lemmatized'] = mdf['lemmatized'].apply(
        lambda x: [word for word in x if word not in stop_words])

    mdf['lemma_str'] = [' '.join(map(str, le)) for le in mdf['lemmatized']]

    Mdf = mdf[["lemma_str", "job_url"]]

    vectorizer = TfidfVectorizer(max_features=300)

    X = vectorizer.fit_transform(Mdf['lemma_str'])

    Vecdf = pd.DataFrame(X.toarray())

    Mdf['vec'] = X.toarray().tolist()

    Mdf['res'] = string_data

    Mdf['mod_res'] = Mdf['res'].apply(lambda x: remove_URL(x))
    Mdf['mod_res'] = Mdf['mod_res'].apply(lambda x: remove_emoji(x))
    Mdf['mod_res'] = Mdf['mod_res'].apply(lambda x: remove_html(x))
    Mdf['mod_res'] = Mdf['mod_res'].apply(lambda x: remove_punct(x))
    Mdf['mod_res'] = Mdf['mod_res'].apply(lambda x: remove_quotes(x))

    Mdf['mod_res'] = Mdf['mod_res'].apply(word_tokenize)

    Mdf['mod_res'] = Mdf['mod_res'].apply(
        lambda x: [word.lower() for word in x])
    Mdf['mod_res'] = Mdf['mod_res'].apply(
        lambda x: [word for word in x if word not in stop_words])

    Mdf['mod_res'] = Mdf['mod_res'].apply(nltk.tag.pos_tag)

    Mdf['mod_res'] = Mdf['mod_res'].apply(
        lambda x: [(word, get_wordnet_pos(pos_tag)) for (word, pos_tag) in x])

    wnl = WordNetLemmatizer()

    Mdf['mod_res'] = Mdf['mod_res'].apply(
        lambda x: [wnl.lemmatize(word, tag) for word, tag in x])

    Mdf['mod_res'] = Mdf['mod_res'].apply(
        lambda x: [word for word in x if word not in stop_words])

    Mdf['mod_res'] = [' '.join(map(str, le)) for le in Mdf['mod_res']]

    res_matrix = vectorizer.transform(Mdf['mod_res']).toarray().tolist()

    Mdf['vec_res'] = res_matrix

    a = Mdf['vec'].map(lambda x: np.array(x))

    b = Mdf['vec_res'].map(lambda x: np.array(x))

    Mdf['score'] = (a*b).map(lambda x: sum(x))

    final = Mdf.sort_values('score', ascending=False)

    ret_df = pd.DataFrame(columns=["job_title", "company_name", "posted_date", "job_url"])
    for i, url in enumerate(final.head(5)['job_url'].to_numpy()):
        ret_df = pd.concat([ret_df, df[df['job_url']==url][["job_title", "company_name", "posted_date", "job_url"]]])

    return ret_df