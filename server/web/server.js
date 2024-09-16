const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const port = process.env.PORT || 3100;

// Прокси-конфигурация для API
app.use('/api/v1', createProxyMiddleware({
  target: 'http://195.2.81.46:9999/api/v1',
  changeOrigin: true,
  secure: false, // Разрешить использование http
}));

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
