# Revisão técnica — arquitetura do TechFix

## Escopo desta revisão
Esta revisão registra as decisões estruturais previstas para o MVP. O repositório ainda está na etapa de documentação; portanto, os pontos abaixo orientam a implementação e não afirmam que as camadas já estejam codificadas.

## Modularização
A aplicação seguirá uma arquitetura monolítica organizada em camadas:
- **Rotas:** recebem requisições HTTP e direcionam as operações.
- **Modelos:** representam Cliente, Equipamento e OrdemServico e sua persistência.
- **Templates:** concentram a apresentação com Jinja2.
- **Serviços/regras de aplicação:** concentram validações e operações que não devem ficar duplicadas nas rotas.

Essa separação reduz acoplamento e facilita manutenção e testes.

## Persistência e desempenho
O SQLite atende ao escopo inicial de um MVP individual e reduz a complexidade de implantação. As consultas deverão utilizar os relacionamentos definidos entre cliente, equipamento e ordem de serviço, evitando leituras repetidas desnecessárias. Caso o volume ou a concorrência cresçam, a camada de persistência poderá ser migrada sem reescrever a interface.

## Segurança e qualidade
As entradas serão validadas no servidor; senhas, quando houver autenticação implementada, deverão ser armazenadas somente com hash apropriado (scrypt ou PBKDF2). As rotas restritas deverão exigir autenticação. Testes automatizados deverão cobrir as operações centrais antes da evolução do MVP.

## Resultado da auto-revisão
A estrutura proposta é compatível com o escopo e mantém a solução simples. A implementação deverá preservar a separação entre apresentação, regras de aplicação e persistência, evitando concentrar toda a lógica em um único arquivo.
