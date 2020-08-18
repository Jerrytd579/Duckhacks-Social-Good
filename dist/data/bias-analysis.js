const { PredictionServiceClient } = require('@google-cloud/automl').v1;

const axios = require('axios');
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
    return axios
      .post('http://127.0.0.1:5000/analyze', { text: content })
      .then((res) => {
        return res;
      })
      .catch((err) => {
        // console.log(err);
      });
  },
};
