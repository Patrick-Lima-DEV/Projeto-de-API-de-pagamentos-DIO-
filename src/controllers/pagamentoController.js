// Simulação de dados em memória
let pagamentos = [];

exports.listarPagamentos = (req, res) => {
  res.json(pagamentos);
};

exports.criarPagamento = (req, res) => {
  const novoPagamento = {
    id: pagamentos.length + 1,
    ...req.body
  };
  pagamentos.push(novoPagamento);
  res.status(201).json(novoPagamento);
};

exports.atualizarPagamento = (req, res) => {
  const { id } = req.params;
  const index = pagamentos.findIndex(p => p.id == id);
  if (index === -1) return res.status(404).json({ erro: 'Pagamento não encontrado' });
  pagamentos[index] = { ...pagamentos[index], ...req.body };
  res.json(pagamentos[index]);
};

exports.deletarPagamento = (req, res) => {
  const { id } = req.params;
  const index = pagamentos.findIndex(p => p.id == id);
  if (index === -1) return res.status(404).json({ erro: 'Pagamento não encontrado' });
  pagamentos.splice(index, 1);
  res.status(204).send();
};
