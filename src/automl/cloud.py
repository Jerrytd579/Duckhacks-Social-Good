import os
from google.cloud import automl

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gauth.json'
project_id = 'algebraic-depot-286523'
model_id = 'TST4181277793687961600'

prediction_client = automl.PredictionServiceClient()

# Get the full path of the model.
model_full_id = prediction_client.model_path(project_id, 'us-central1', model_id)

def cloud_predict(content: str):
    text_snippet = automl.types.TextSnippet(content=content, mime_type='text/plain')
    payload = automl.types.ExamplePayload(text_snippet=text_snippet)
    response = prediction_client.predict(model_full_id, payload)
    print(response)
    return response.metadata['sentiment_score']

result = cloud_predict('this is racist')
print(result)
