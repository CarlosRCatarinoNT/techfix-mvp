# Modelo de dados — TechFix

O MVP utiliza SQLite para armazenar as informações da assistência técnica.

## Cliente
- id: identificador único.
- nome: nome do cliente.
- telefone: telefone para contato.
- email: endereço de e-mail (opcional).

## Equipamento
- id: identificador único.
- cliente_id: referência ao cliente proprietário.
- tipo: tipo de equipamento.
- marca: fabricante.
- modelo: modelo do equipamento.
- numero_serie: identificação/serial (quando disponível).

## OrdemServico
- id: identificador único.
- cliente_id: referência ao cliente.
- equipamento_id: referência ao equipamento.
- descricao_problema: relato do defeito informado.
- diagnostico: avaliação técnica (opcional no cadastro inicial).
- orcamento: valor previsto (opcional).
- status: situação atual da ordem de serviço.
- data_abertura: data de criação da ordem.

## Relacionamentos
- Um cliente pode possuir vários equipamentos.
- Um cliente pode abrir várias ordens de serviço.
- Um equipamento pode estar associado a várias ordens ao longo do tempo.
- Cada ordem de serviço referencia um cliente e um equipamento.