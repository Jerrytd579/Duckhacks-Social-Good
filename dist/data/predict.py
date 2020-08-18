import pickle
import re
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer

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

vectorizer = pickle.load(open('vectorizer.pk', 'rb'))
classifier = pickle.load(open('classifier.pk', 'rb'))

def predict(text: str) -> float:
    """Given a string of text, performs a sentiment analysis and returns a score of [0,1].
    The model's data is vectorized using TF-IDF, and learns using a Bagging Classifier model."""
    data = vectorizer.transform([text])
    return classifier.predict_proba(data)[0][1]

# while True:
#     text = input('> ')
#     result = predict(text)
#     print(f'{result:.2%} racial bias')

# Server
from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        text = request.json['text']
        value = predict(text)
        return value

app.run()
