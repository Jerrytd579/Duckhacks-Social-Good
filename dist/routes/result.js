const express = require('express');
const fs = require('fs');
const router = express.Router();
const data = require('../data/bias-analysis');

process.env.GOOGLE_APPLICATION_CREDENTIALS = 'data/gauth.json';

router.post('/result', async (req, res) => {
  const formData = req.body;

  if (!formData['text-to-test']) {
    res.status(400);
    res.render('result/result', {
      title: 'Bias Analyzer Results Error',
      errors: true,
    });
    return;
  }
  try {
    let query = formData['text-to-test'];
    console.log('query', query);
    const score = await data.predict(query);
    let text = '';
    switch (score) {
      case score >= 0.45 && score <= 0.55:
        text = 'This text is most likely neutral.';
        break;
      case score > 0.55 && score <= 0.65:
        text = 'This text may contain racial bias.';
        break;
      case score > 0.65:
        text = 'This text is very likely racist!';
        break;
      case score < 0.45 && score >= 0.35:
        text = 'This text is probably not discriminatory.';
        break;
      case score < 0.35:
        text = 'This text is very unlikely to contain racial bias.';
        break;
    }
    res.render('result/result', {
      title: 'Bias Analysis Results',
      text: text,
      score: score,
    });
  } catch (e) {
    res.status(500).json({ error: e });
  }
});

module.exports = router;
