import json
import requests

API = 'https://api.hatebase.org/4-4/{}'
auth = requests.post(API.format('authenticate'), data={
    'api_key': 'eVYUGZXGPPBcdbXnCPdNWtEhtFgKuJpR'
})
token = auth.json()['result']['token']
bad_words = set()
for page in range(1, 50):
    data = requests.post(API.format('get_sightings'), data={
        'token': token,
        'year': 2019,
        'is_about_ethnicity': True,
        'language': 'ENG',
        'page': page,
    })
    out = data.json()
    for result in out['result']:
        bad_words.add(result['term'])
with open('hatebase.txt', 'w') as f:
    f.write('\n'.join(bad_words))
