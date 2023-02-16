from utils import pp, array_from_file


import nltk
from nltk import ne_chunk, pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

from nltk.stem import WordNetLemmatizer

from bs4 import BeautifulSoup
import requests
from langdetect import detect
import re

import sqlite3



nltk_dir = './nltk_data'
nltk.data.path.append(nltk_dir)

ALLOWED_LANGUAGES = array_from_file('./data/allowed_languages.json')

if not ALLOWED_LANGUAGES:
    ALLOWED_LANGUAGES = ['english']


nltk.download('punkt', download_dir=nltk_dir)
nltk.download('averaged_perceptron_tagger', download_dir=nltk_dir)
nltk.download('maxent_ne_chunker', download_dir=nltk_dir)
nltk.download('words', download_dir=nltk_dir)
nltk.download('stopwords', download_dir=nltk_dir)
nltk.download('wordnet', download_dir=nltk_dir)
# nltk.download('vader_lexicon', download_dir=nltk_dir)


def clear_cache_data(age_days=7):
    import os
    import time
    cache_dir = '.cache'

    # Get the current time in seconds
    now = time.time()

    # Loop through all files in the cache directory
    for filename in os.listdir(cache_dir):
        filepath = os.path.join(cache_dir, filename)

        # Get the age of the file in seconds
        age = now - os.path.getmtime(filepath)

        # If the file is older than the specified age, delete it
        if age > age_days * 86400:
            os.remove(filepath)

def get_article_contents(url):
    html = read_article_from_url(url)
    soup = BeautifulSoup(html, 'html.parser')
    article = ''
    for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        article += element.text + '\n'

    return article

def read_article_from_url(url):
    # print(f"Reading article from {url}...")
    
    import hashlib
    import os
    import requests
    
    # Convert url to md5 hash
    url_md5 = hashlib.md5(url.encode('utf-8')).hexdigest()

    # Check if article exists in '.cache' folder
    cache_dir = '.cache'
    cache_path = os.path.join(cache_dir, url_md5)
    if os.path.exists(cache_path):
        # If it does, return the contents of the file
        with open(cache_path, 'r') as f:
            return f.read()
    else:
        # If it doesn't, try using Google's cached version of the article
        print(f"Reading article from {url}...")
        try:
            google_cache_url = f"http://webcache.googleusercontent.com/search?q=cache:{url}"
            response = requests.get(google_cache_url)
            response.raise_for_status()  # Raise exception for non-200 status codes
            contents = response.text

            # Create cache directory if it doesn't exist
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir)

            # Write contents to cache file
            with open(cache_path, 'w') as f:
                f.write(contents)

            return contents
        except requests.exceptions.HTTPError:
            # If Google's cached version is not available, download the article and save it to the cache
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise exception for non-200 status codes
                contents = response.text

                # Create cache directory if it doesn't exist
                if not os.path.exists(cache_dir):
                    os.makedirs(cache_dir)

                # Write contents to cache file
                with open(cache_path, 'w') as f:
                    f.write(contents)

                return contents
            except requests.exceptions.HTTPError as e:
                print(f"Error retrieving article from {url}: {e}")


def detect_language(article):
    LANGUAGE_MAP = {
        'ar': 'arabic',
        'az': 'azerbaijani',
        'basque': 'basque',
        'bn': 'bengali',
        'ca': 'catalan',
        'chinese': 'chinese',
        'da': 'danish',
        'dutch': 'dutch',
        'en': 'english',
        'fi': 'finnish',
        'fr': 'french',
        'de': 'german',
        'el': 'greek',
        'he': 'hebrew',
        'hinglish': 'hinglish',
        'hu': 'hungarian',
        'id': 'indonesian',
        'it': 'italian',
        'kk': 'kazakh',
        'ne': 'nepali',
        'no': 'norwegian',
        'pt': 'portuguese',
        'ro': 'romanian',
        'ru': 'russian',
        'sl': 'slovene',
        'es': 'spanish',
        'sv': 'swedish',
        'tg': 'tajik',
        'tr': 'turkish'
    }

    language_code = detect(article)
    language = LANGUAGE_MAP.get(language_code)
    return language

def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()

    # Remove non-alphanumeric characters
    text = re.sub(r'[^a-z0-9 ]+', '', text)

    # Tokenize the text into words
    tokens = word_tokenize(text)

    # Remove stopwords and lemmatize the remaining words
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words and len(word) > 2]

    # Join the tokens back into a string
    text = ' '.join(tokens)

    return text

def vectorize_text(preprocessed_contents_list):
    # Create a TfidfVectorizer object with custom options
    vectorizer = TfidfVectorizer(
        max_features=5000, # Maximum number of features to include in the vectorization
        ngram_range=(1, 3), # Range of n-gram sizes to include (1-3 words)
        sublinear_tf=True, # Apply sublinear scaling to term frequency counts
        stop_words='english' # Ignore stop words in the English language
    )

    # Fit the vectorizer to the preprocessed article contents
    X = vectorizer.fit_transform(preprocessed_contents_list)

    # Get the feature names (i.e., words) from the vectorizer
    feature_names = vectorizer.get_feature_names_out()

    return X, feature_names

def train_data(good_articles, bad_articles):
    # Preprocess the text in the good and bad article lists
    preprocessed_good = [preprocess_text(get_article_contents(article)) for article in good_articles]
    preprocessed_bad =  [preprocess_text(get_article_contents(article)) for article in bad_articles]

    # Create the training data matrix by combining the preprocessed good and bad article text
    x_train, feature_names = vectorize_text(preprocessed_good + preprocessed_bad)

    # Create the labels for the training data (1 for good articles, 0 for bad articles)
    y_train = [1] * len(preprocessed_good) + [0] * len(preprocessed_bad)

    # Train a linear support vector machine (SVM) model on the training data
    svm = LinearSVC()
    svm.fit(x_train, y_train)

    return svm, feature_names
    
def test_data(good_articles, bad_articles):
    # Split the good and bad articles into training and testing sets
    good_train, good_test = train_test_split(good_articles, test_size=0.2)
    bad_train, bad_test = train_test_split(bad_articles, test_size=0.2)

    # Preprocess the text in the training and testing sets
    preprocessed_good_train = [preprocess_text(get_article_contents(article)) for article in good_train]
    preprocessed_bad_train = [preprocess_text(get_article_contents(article)) for article in bad_train]
    preprocessed_good_test = [preprocess_text(get_article_contents(article)) for article in good_test]
    preprocessed_bad_test = [preprocess_text(get_article_contents(article)) for article in bad_test]

    # Create the training data matrix by combining the preprocessed good and bad article text
    x_train, feature_names = vectorize_text(preprocessed_good_train + preprocessed_bad_train)

    # Create the labels for the training data (1 for good articles, 0 for bad articles)
    y_train = [1] * len(preprocessed_good_train) + [0] * len(preprocessed_bad_train)

    # Train a linear support vector machine (SVM) model on the training data
    svm = LinearSVC()
    svm.fit(x_train, y_train)

    # Create the testing data matrix by combining the preprocessed good and bad article text
    x_test, _ = vectorize_text(preprocessed_good_test + preprocessed_bad_test)

    # Create the labels for the testing data (1 for good articles, 0 for bad articles)
    y_test = [1] * len(preprocessed_good_test) + [0] * len(preprocessed_bad_test)


    # Use the trained SVM model to make predictions on the test data
    y_pred = svm.predict(x_test)

    # Create a confusion matrix of the test results
    cm = confusion_matrix(y_test, y_pred)

    # Evaluate the model's accuracy on the testing data
    accuracy = svm.score(x_test, y_test)

    print(f"Accuracy: {accuracy:.2f}\n")
    print(f"confusion_matrix:\n{cm}")

    return accuracy















if __name__ == '__main__':
    print('\n' * 8)
    clear_cache_data(1)

    conn = sqlite3.connect('./data/trendman.db')
    # Create a cursor
    cursor = conn.cursor()

    GOOD_ARTICLES = []
    BAD_ARTICLES = []

    # Get the good articles
    good_articles = cursor.execute("SELECT * FROM processed WHERE score = 1").fetchall()
    for article in good_articles:
        GOOD_ARTICLES.append(article[0])

    # Get the bad articles
    bad_articles = cursor.execute("SELECT * FROM processed WHERE score = 0").fetchall()
    for article in bad_articles:
        BAD_ARTICLES.append(article[0])


    url = 'https://noahberlatsky.substack.com/p/why-white-students-need-black-history'


    pp(BAD_ARTICLES)

    # accuracy = test_data(GOOD_ARTICLES, BAD_ARTICLES)


