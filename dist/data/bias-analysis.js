const { PredictionServiceClient } = require('@google-cloud/automl').v1;

const client = new PredictionServiceClient();
const projectId = 'algebraic-depot-286523';
const location = 'us-central1';
const modelId = 'TST4181277793687961600';

module.exports = {
  async predict_cloud(content) {
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

    const [res] = await client.predict(request);
    let predict = res.payload[0].textSentiment.sentiment;
    let score = res.metadata.sentiment_score;
    return predict, score;
  },
  async predict(content) {
    return await fetch('http://localhost:5000/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: content,
      }),
    });
  },
};
