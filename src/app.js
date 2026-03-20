require('dotenv').config();
const express = require('express');
const pagamentoRoutes = require('./routes/pagamentoRoutes');
const authRoutes = require('./routes/authRoutes');
const { autenticarToken } = require('./middlewares/authMiddleware');
const rateLimitMiddleware = require('./middlewares/rateLimitMiddleware');

const app = express();
app.use(express.json());

app.use('/auth', authRoutes);
app.use('/pagamentos', rateLimitMiddleware, autenticarToken, pagamentoRoutes);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
});
