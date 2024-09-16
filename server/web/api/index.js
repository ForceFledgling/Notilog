const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const port = process.env.PORT || 3100;

// Прокси-конфигурация (при необходимости)
app.use('/api/v1', createProxyMiddleware({
  target: 'http://195.2.81.46:9999',
  changeOrigin: true,
  secure: false, // Разрешить использование http
}));

// Обслуживание статических файлов из директории dist
app.use(express.static(path.join(__dirname, 'dist')));


app.get('/', (req, res) => {
  console.log('Requested path:', req.path); // Добавьте это для отладки
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

// Обработка всех остальных запросов
app.get('*', (req, res) => {
  console.log('Requested path:', req.path); // Добавьте это для отладки
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

export default app