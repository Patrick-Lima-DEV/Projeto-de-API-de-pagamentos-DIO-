const jwt = require('jsonwebtoken');
const { SECRET } = require('../middlewares/authMiddleware');

// Usuário fixo para simulação
const usuarioDemo = {
  id: 1,
  nome: 'usuario_demo',
  senha: 'senha123'
};

exports.login = (req, res) => {
  const { nome, senha } = req.body;
  if (nome !== usuarioDemo.nome || senha !== usuarioDemo.senha) {
    return res.status(401).json({ erro: 'Credenciais inválidas' });
  }
  const token = jwt.sign({ id: usuarioDemo.id, nome: usuarioDemo.nome }, SECRET, { expiresIn: '1h' });
  res.json({ token });
};
