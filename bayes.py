import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.classify import NaiveBayesClassifier

from utils import pp, array_from_file

nltk_dir = './nltk_data'
nltk.data.path.append(nltk_dir)

nltk.download('punkt', download_dir=nltk_dir)
nltk.download('averaged_perceptron_tagger', download_dir=nltk_dir)
nltk.download('maxent_ne_chunker', download_dir=nltk_dir)
nltk.download('words', download_dir=nltk_dir)
nltk.download('stopwords', download_dir=nltk_dir)

# tokenize the text into sentences
text = "Sample text containing a full article."
sentences = sent_tokenize(text)

# clean the text
cleaned_sentences = []
for sentence in sentences:
    words = word_tokenize(sentence.lower())
    words = [word for word in words if word.isalpha() and word not in stopwords.words('english')]
    cleaned_sentences.append(words)

# extract features
def get_features(sentence):
    words = set(sentence)
    features = {}
    for word in words:
        features[word] = True
    return features

labeled_data = [('sentence 1', 'topic 1'), ('sentence 2', 'topic 2')]
training_data = [(get_features(sentence), topic) for sentence, topic in labeled_data]

pp(training_data)
exit()

# train the classifier
classifier = NaiveBayesClassifier.train(training_data)

# classify the article
article_features = [get_features(sentence) for sentence in cleaned_sentences]
predicted_topics = [classifier.classify(features) for features in article_features]
print(predicted_topics)
