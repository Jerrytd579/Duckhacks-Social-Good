const indexRoutes = require('./form');
const resultRoutes = require('./result');
const path = require('path');

const constructorMethod = (app) => {
  app.use('/', indexRoutes);
  app.use('/result', resultRoutes);
  app.use('*', (req, res) => {
    res.redirect('/');
  });
};

module.exports = constructorMethod;
