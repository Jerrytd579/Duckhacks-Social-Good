import csv
import nltk
import pickle
import re
from typing import ItemsView

from nltk.corpus import stopwords, wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from scipy.sparse import save_npz, load_npz
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split

# Classifiers
from sklearn.ensemble import BaggingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB


print('>> Preparing training/test data set')
raw_data = []
scores = []
with open('prep/training_data.csv', encoding='utf-8') as f:
    r = csv.reader(f, dialect='excel')
    for line in r:
        raw_data.append(line[0])
        scores.append(line[1])
print(f'>> {scores.count("0")} non-discrimantory, {scores.count("1")} discriminatory entities')

# Split data into training/test set
raw_train, raw_test, y_train, y_test = train_test_split(
    raw_data, scores, test_size=0.25, random_state=42)

# Lemma Tokenizer
class LemmaTokenizer:
    def __init__(self):
        self.wnl = WordNetLemmatizer()
        self.stopwords = stopwords.words('english')
        self.pos_map = {
            'J': wordnet.ADJ,
            'V': wordnet.VERB,
            'R': wordnet.ADV,
        }
        self.token = re.compile(r'^[a-zA-Z]{3,}$')

    def __call__(self, articles):
        # Remove stopwords (and, if, the, a, etc.)
        words = filter(lambda w: w not in self.stopwords, nltk.word_tokenize(articles))
        # Get part of speech for lemmas
        tagged = nltk.pos_tag(list(words))
        # Only keep characters a-z
        tokens = filter(lambda w: self.token.match(w[0]), tagged)
        return [self.wnl.lemmatize(word, pos=self.pos_map.get(pos[0], wordnet.NOUN)) for word, pos in tokens]

# print('>> Creating BOW model')
# # Bag of words (BOW) model
# vectorizer = CountVectorizer(
#     min_df=1,
#     ngram_range=(1, 2),
#     strip_accents='ascii',
#     tokenizer=LemmaTokenizer(),
#     token_pattern=None,)
# vectorizer.fit(raw_train)

print('>> Creating TF-IDF model')
# TF-IDF model
vectorizer = TfidfVectorizer(
    min_df=1,
    ngram_range=(1, 2),
    strip_accents='ascii',
    tokenizer=LemmaTokenizer(),
    token_pattern=None,)
vectorizer.fit(raw_train)
pickle.dump(vectorizer, open('vectorizer.pk', 'wb'))

x_train = vectorizer.transform(raw_train)
x_test = vectorizer.transform(raw_test)

print('>> Running predictions on ML models')
# Multinomial Naive Bayes Model
nb_classifier = MultinomialNB().fit(x_train, y_train)
score = nb_classifier.score(x_test, y_test)
print(f'MNB Model Test Accuracy: {score:.2%}')

# Simple logistic regression model
lr_classifier = LogisticRegression().fit(x_train, y_train)
score = lr_classifier.score(x_test, y_test)
print(f'LR Model Test Accuracy: {score:.2%}')

# Bagging Classifier Model
bc_classifier = BaggingClassifier().fit(x_train, y_train)
score = bc_classifier.score(x_test, y_test)
print(f'BC Model Test Accuracy: {score:.2%}')
pickle.dump(bc_classifier, open('classifier.pk', 'wb'))

def evaluate(query: str) -> ItemsView[str, float]:
    """Given a string input, returns the results of each model's prediction.
    This should eventually return a float with the best overall accuracy for the web."""
    test = vectorizer.transform([query])
    return {
        'MNB Model': nb_classifier.predict_proba(test)[0][1],
        'LR Model': lr_classifier.predict_proba(test)[0][1],
        'BC Model': bc_classifier.predict_proba(test)[0][1],
    }.items()

print('Enter your queries after the \'>\' to get an estimate. Type \'quit\' to quit.')
while True:
    query = input('> ')
    if query == 'quit':
        exit()
    assert query != ''
    print()
    for result, accuracy in evaluate(query):
        print(f'{result}: {accuracy:.2%} likely to include racial bias')
    print()
