const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const port = process.env.PORT || 3100;

// Прокси для API-запросов
app.use('/api/v1', createProxyMiddleware({
  target: 'http://195.2.81.46:9999/api/v1',
  changeOrigin: true,
  secure: false
}));

// Обслуживание статических файлов из папки dist
app.use(express.static(path.join(__dirname, 'dist')));

// Все запросы кроме API направляем на index.html
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
