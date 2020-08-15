# import json
# ids = {}
# with open('hatespeech_2.csv') as f:
#     lines = f.readlines()
#     for l in lines:
#         id_, tag = l.strip().split(',')
#         ids[id_] = tag == 'racism'
# with open('hatespeechtwitter.csv') as f:
#     lines = f.readlines()[1:]
#     for l in lines:
#         id_, tag = l.strip().split(',')
#         if tag == 'spam':
#             continue
#         racist = tag in ('abusive', 'hateful')
#         ids[id_] = racist
# with open('tweets.json', 'w') as f:
#     json.dump(ids, f, indent=2)

import csv
racist = []
not_racist = []
with open('data/tweets.csv', encoding='utf-8') as f:
    r = csv.reader(f, dialect='excel')
    for line in r:
        if line[1] == 'True':
            racist.append(line[0])
        else:
            not_racist.append(line[0])

with open('data/tweets_split.csv', 'w', newline='\n', encoding='utf-8') as f:
    w = csv.writer(f, dialect='excel')
    for tweet in racist:
        w.writerow([tweet, 1])
    for tweet in not_racist[:len(racist)]:
        w.writerow([tweet, 0])
