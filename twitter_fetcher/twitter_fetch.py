import tweepy

# Developer keys
consumer_key = 'n7XodB4xRIBS74OcP4ixkkDez'
consumer_key_secret = 'BqM2Qm9tfqj6XSuDX6vC9ChSssZQ1lnNcw3bnTjKpCeAFN7KRQ'
access_token = '2959509513-oo3kPYnKcwmP2MpyUXKYuN6PTEt9oKb7ri3Fjng'
access_token_secret = 'qG04qVhIZjz06ETbcZ4AWFDcRHUl2knJ8JjwZ9aBBuglW'

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def createTrainingSet(corpusFile, targetResultFile):
    import csv
    import time

    counter = 0
    corpus = []

    with open(corpusFile, 'r') as csvfile:
        lineReader = csv.reader(csvfile, delimiter=',', quotechar="\"")
        for row in lineReader:
            corpus.append({"tweet_id": row[0]})

    sleepTime = 2
    trainingDataSet = []

    for tweet in corpus:
        try:
            tweetFetched = api.get_status(tweet["tweet_id"])
            print("Tweet fetched: " + tweetFetched.text)
            tweet["text"] = tweetFetched.text
            trainingDataSet.append(tweet)
            time.sleep(sleepTime)

        except:
            print("Inside the exception - no:2")
            continue

    with open(targetResultFile, 'w') as csvfile:
        linewriter = csv.writer(csvfile, delimiter=',', quotechar="\"")
        for tweet in trainingDataSet:
            try:
                linewriter.writerow([tweet["tweet_id"], tweet["text"]])
            except Exception as e:
                print(e)
    return trainingDataSet

# Code starts here
# This is the dataset
corpusFile = "datasets/test_tweet_fetch.csv"
# This is my target file
targetResultFile = "datasets/test_tweet_target.csv"
# Call the method
resultFile = createTrainingSet(corpusFile, targetResultFile)