const express = require('express');
const fs = require('fs');
const router = express.Router();
const data = require('../data/bias-analysis');

process.env.GOOGLE_APPLICATION_CREDENTIALS = 'data/gauth.json';

router.post('/', async (req, res) => {
  const formData = req.body;

  if (!formData['text-to-test']) {
    res.status(400);
    res.render('result/result', {
      title: 'Bias Analyzer Results Error',
      errors: true,
    });
    return;
  }
  let query = formData['text-to-test'];
  const score = await data.predict(query);
  let index = 0;
  let text = 'CHECK THIS';
  if(score >= 0.45 && score <= 0.55){
    text = 'This text is most likely neutral.';
    index= 3;
  }else if(score > 0.55 && score <= 0.65){
      text = 'This text may contain racial bias.';
      index= 4;
  }else if(score > 0.65){
      text = 'This text is very likely racist!';
      index= 5;
  }else if(score < 0.45 && score >= 0.35){
    text = 'This text is probably not discriminatory.';
    index= 2;
  }else if(score == 0){
    text = 'This text is very unlikely to contain racial bias.';
    index= 1;
    console.log("hereeee");
  }else{
    text = 'This text is very unlikely to contain racial bias.';
    index= 1;
    console.log("noooooo");
  }
  console.log("_____________________________________________________ggggggggggg________________");
  console.log(score);
  console.log(text);
  if(index == 1){
    console.log("nooooo1111");
    res.render('result/result', {
      title: 'Bias Analysis Results',
      text: text,
      score: score,
      one:true
    });
  
  }else
  if(index == 2){
    res.render('result/result', {
      title: 'Bias Analysis Results',
      text: text,
      score: score,
      two:true
    });
  }else
  if(index == 3){
    res.render('result/result', {
      title: 'Bias Analysis Results',
      text: text,
      score: score,
      three:true
    });
  }else
  if(index == 4){
    res.render('result/result', {
      title: 'Bias Analysis Results',
      text: text,
      score: score,
      four:true
    });
  }else
    res.render('result/result', {
      title: 'Bias Analysis Results',
      text: text,
      score: score,
      five:true
    });
  
});

module.exports = router;
