from utils import pp


import nltk
from nltk import ne_chunk, pos_tag
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
import requests
from langdetect import detect
import re

nltk_dir = './nltk_data'
nltk.data.path.append(nltk_dir)

nltk.download('punkt', download_dir=nltk_dir)
nltk.download('averaged_perceptron_tagger', download_dir=nltk_dir)
nltk.download('stopwords', download_dir=nltk_dir)
nltk.download('wordnet', download_dir=nltk_dir)
nltk.download('vader_lexicon', download_dir=nltk_dir)
nltk.download('maxent_ne_chunker', download_dir=nltk_dir)
nltk.download('words', download_dir=nltk_dir)

def extract_tags_from_url(url):
    # Download and parse the HTML content of the article
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Extract the article content from the HTML
    article = ''
    for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        article += element.text + '\n'

    # Detect the language of the article
    language_code = detect(article)
    language = LANGUAGE_MAP.get(language_code)

    # Perform POS tagging on the article text
    tagged_words = pos_tag(word_tokenize(article))

    # Identify named entities
    named_entities = ne_chunk(tagged_words)

    # Extract the named entities from the tree structure
    named_entities = [chunk for chunk in named_entities if hasattr(chunk, 'label')]

    # Extract unique named entities, ordered by frequency
    named_entities = [entity for entity in named_entities if len(entity) > 1]
    named_entities = [entity for entity in named_entities if entity.label() in ['PERSON', 'ORGANIZATION', 'GPE']]
    

    pp(named_entities)

    # Return the list of tags and the detected language
    return [], language


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



if __name__ == '__main__':
    url = 'https://www.lifewire.com/why-mastodon-apps-should-stop-trying-to-copy-twitter-7109967'
    tags, language = extract_tags_from_url(url)
    print(tags, language)



