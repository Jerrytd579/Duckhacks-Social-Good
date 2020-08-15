import csv

with open('data/tweets.csv', encoding='utf-8') as f:
    r = csv.reader(f)
    with open('data/tweets_gcloud.csv', 'w', newline='\n', encoding='utf-8') as fo:
        w = csv.writer(fo, dialect='excel')
        for line in r:
            if len(line) == 0:
                continue
            formatted = [line[0], 1 if line[1] == 'True' else 0]
            w.writerow(formatted)
