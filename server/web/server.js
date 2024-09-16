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

// Обслуживание статических файлов из директории dist
app.use(express.static(path.join(__dirname, 'dist')));

// Отдавать index.html для всех маршрутов, кроме API
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
