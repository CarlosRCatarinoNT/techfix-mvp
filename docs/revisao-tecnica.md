# Revisão técnica do MVP TechFix

## Arquitetura e modularização

O MVP seguirá uma arquitetura monolítica em camadas. A separação entre modelos, rotas, templates e arquivos estáticos reduz o acoplamento e facilita a manutenção. A camada de modelos concentra o acesso aos dados; as rotas recebem as requisições e coordenam as operações; os templates cuidam da apresentação.

O SQLite atende ao escopo inicial e evita a necessidade de administrar um servidor de banco de dados separado. As consultas devem permanecer objetivas e utilizar os recursos do ORM para manter consistência. Caso o volume de uso cresça, a camada de persistência poderá ser substituída sem reescrever a interface.

## Segurança e qualidade

A aplicação deverá validar os dados recebidos no servidor, mesmo quando houver validação no navegador. Senhas, quando a autenticação for implementada, deverão ser armazenadas somente com hash apropriado (scrypt ou PBKDF2), nunca em texto puro ou com MD5/SHA-1.

As rotas privadas deverão exigir autenticação e autorização. Mensagens de erro apresentadas ao usuário não devem expor detalhes internos, caminhos ou informações sensíveis. As operações com banco deverão utilizar parâmetros/ORM, evitando montar comandos SQL por concatenação.

## Escopo desta revisão

Este documento registra decisões e critérios técnicos para orientar a implementação. Como o repositório ainda está na etapa de documentação, os controles descritos são diretrizes a implementar e verificar por testes; não representam funcionalidades já concluídas.
