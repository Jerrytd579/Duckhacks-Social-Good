import csv
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Naive Bayes
# from nltk import NaiveBayesClassifier
from sklearn.naive_bayes import MultinomialNB

with open('../prep/data/tweets_gcloud.csv', encoding='utf-8') as f:
    r = csv.reader(f, dialect='excel')
    tweets = []
    scores = []
    for line in r:
        tweets.append(line[0])
        scores.append(line[1])

# Split data into training/test set
tweet_train, tweet_test, y_train, y_test = train_test_split(
    tweets, scores, test_size=0.25, random_state=42)

# Lemma Tokenizer
class LemmaTokenizer:
    def __init__(self):
        self.wnl = WordNetLemmatizer()

    def __call__(self, articles):
        return [self.wnl.lemmatize(t) for t in nltk.word_tokenize(articles)]

# Bag of words (BOW) model
vectorizer = CountVectorizer(
    min_df=0,
    stop_words=stopwords.words('english'),
    token_pattern=r'\b[a-zA-Z]{2,}\b',
    tokenizer=LemmaTokenizer())
vectorizer.fit(tweet_train)
x_train = vectorizer.transform(tweet_train)
x_test = vectorizer.transform(tweet_test)

# Simple logistic regression model
lr_classifier = LogisticRegression()
lr_classifier.fit(x_train, y_train)
score = lr_classifier.score(x_test, y_test)
print(f'LR Model Accuracy: {score:.2%}')
# LR Model: 98.24% accuracy?

# Multinomial Naive Bayes Model
nb_classifier = MultinomialNB().fit(x_train, y_train)
predicted = nb_classifier.predict(x_test)
score = metrics.accuracy_score(y_test, predicted)
print(f'MNB Model Accuracy: {score:.2%}')

sample_cases = [
    'I hate niggers.',
    'I like pineapple pizza.',
    'I will murder the Jews.',
    'Those girls are boring Asians.',
    'I like to rock climb.',
    'I have no idea what I want to say.',
    'Do you watch The Office on Netflix?',
]
new_test = vectorizer.transform(sample_cases)
print(nb_classifier.predict(new_test))
print(lr_classifier.predict(new_test))

# NLTK Naive Bayes Model
# train_data = list(zip(tweet_train, y_train))
# test_data = list(zip(tweet_test, y_test))
# nb_classifier = NaiveBayesClassifier.train(train_data)
# print(f'NB Model Accuracy: ', nltk.classify.accuracy(nb_classifier, test_data))
