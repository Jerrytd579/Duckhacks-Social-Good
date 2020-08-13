const express = require('express');
const router = express.Router();
const data = require('../data/bias-analysis');

router.post('/', async (req, res) => {
    const formData = req.body;

    if (!formData['text-to-test']) {
        res.status(400);
        res.render('result/result', {
          title:"Bias Analyzer Results Error",
          errors: true
      });
      return;
    }
    try {
      const results = await data.check(formData['text-to-test']);
      res.render('result/result', {
        title:"Bias Analysis Results",
        text : formData['text-to-test'],
        analysis: results 
      });
      
    } catch (e) {
      res.status(500).json({error: e});
    }
  });
  module.exports = router;