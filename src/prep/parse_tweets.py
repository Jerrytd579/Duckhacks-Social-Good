import json
ids = {}
with open('hatespeech_2.csv') as f:
    lines = f.readlines()
    for l in lines:
        id_, tag = l.strip().split(',')
        ids[id_] = tag == 'racism'
with open('hatespeechtwitter.csv') as f:
    lines = f.readlines()[1:]
    for l in lines:
        id_, tag = l.strip().split(',')
        if tag == 'spam':
            continue
        racist = tag in ('abusive', 'hateful')
        ids[id_] = racist
with open('tweets.json', 'w') as f:
    json.dump(ids, f, indent=2)
