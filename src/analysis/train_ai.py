import csv
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

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
# Bag of words (BOW) model
vectorizer = CountVectorizer(
    min_df=0,
    stop_words=stopwords.words('english'),
    token_pattern=r'\b[a-zA-Z]{2,}\b')
vectorizer.fit(tweet_train)
x_train = vectorizer.transform(tweet_train)
x_test = vectorizer.transform(tweet_test)

# Simple logistic regression model
classifier = LogisticRegression()
classifier.fit(x_train, y_train)
score = classifier.score(x_test, y_test)
print(f'LR Model Accuracy: {score:.2%}')
# LR Model: 98.24% accuracy?
