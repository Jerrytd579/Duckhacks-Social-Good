import { PredictionServiceClient } from '@google-cloud/automl';

const client = new PredictionServiceClient();

export default async function predict() {
  // Construct request
  const request = {
    name: client.modelPath(projectId, location, modelId),
    payload: {
      textSnippet: {
        content: content,
        mimeType: 'text/plain', // Types: 'test/plain', 'text/html'
      },
    },
  };

  const [response] = await client.predict(request);
  console.log();

  for (const annotationPayload of response.payload) {
    console.log(`Predicted class name: ${annotationPayload.displayName}`);
    console.log(
      `Predicted sentiment score: ${annotationPayload.textSentiment.sentiment}`
    );
  }
}

predict();
