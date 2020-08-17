import csv

DATA_PATH = '../prep/data/'
files = ['public_data_labeled.csv', 'labeled_tweets.csv', 'news.csv', 'expletives.csv']
tweet_ids = set('id')
labels = {
    'Non-offensive': 0,
    'Offensive': 1,
}
counts = {0: 0, 1: 0}
with open('training_data.csv', 'w', encoding='utf-8', newline='\n') as fo:
    w = csv.writer(fo, dialect='excel')
    for i, file in enumerate(files):
        with open(DATA_PATH + file, encoding='utf-8') as f:
            r = csv.reader(f, dialect='excel')
            for line in r:
                if i == 0:
                    label, text = line
                    tag = labels.get(label, -1)
                elif i == 1:
                    id_, label, text = line
                    if id_ in tweet_ids:
                        continue
                    tweet_ids.add(id_)
                    tag = labels.get(label, -1)
                else:
                    text, tag = line[0], int(line[1])
                if tag == -1:
                    continue
                w.writerow([text.strip().replace('\n', ''), tag])
                counts[tag] += 1
print(counts)
