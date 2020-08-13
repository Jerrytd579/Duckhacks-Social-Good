const express = require('express');
const router = express.Router();

router.get('/', async (req, res) => {
  res.render('index/index', {
    title:"Bias Analyzer"
  });
});

module.exports = router;
