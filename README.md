# Anti-Double-Charge Engine

Microserviço Full-Stack de auditoria transacional e idempotência mecânica para prevenção de cobranças indevidas e duplicidade de faturamento pós-cancelamento em sistemas bancários legados.

## 🚀 O Problema de Negócio

Um dos maiores desafios em arquiteturas financeiras legadas (Mainframes e sistemas batch descontinuados) é a perda de sincronia na esteira de faturamento. Quando um cliente encerra voluntariamente sua conta ou realiza uma quebra contratual, a flag de cancelamento pode demorar a propagar para o Ledger de cobrança automática. 

Isso gera anomalias severas: **faturamento continuado e indevido de contas inativadas**, ferindo direitos do consumidor e gerando passivos jurídicos massivos para a instituição financeira.

## 🛠️ A Solução Proposta

Este projeto implementa uma barreira dupla de proteção assíncrona baseada em:

1. **Idempotência Mecânica (Camada transacional):** Intercepção de requisições de rede via chaves hash exclusivas (`Idempotency-Key`) geradas por UUID, garantindo que instabilidades de rede ou cliques duplos não gerem faturamento duplicado na mesma janela de tempo.
2. **Varredura Ativa de Cadastro Obsoleto (Camada de dados):** Validação cruzada O(1) de payloads de faturamento contra repositórios externos de contratos finalizados (`database.json`), expurgando e neutralizando cobranças indevidas antes da liquidação financeira.

## 📦 Estrutura do Repositório

* `main.py`: Core Engine desenvolvido em Python que simula o processamento batch assíncrono, aplicando travas transacionais e logs de auditoria diretamente no console.
* `database.json`: Infraestrutura simulada de dados contendo registros de contratos descontinuados, motivos de encerramento e falhas conhecidas de core banking legados.
* `index.html`: Painel de controle responsivo (Front-End moderno em modo escuro) que consome o banco de dados dinamicamente via Fetch API para exibir os logs de mitigação em tempo real.

## 💻 Como Executar o Motor Back-End

Para testar a resiliência do algoritmo via console, execute o script principal em ambiente Python local:

```bash
python main.py
```

## 🔍 Habilidades Demonstradas
* Lógica Transacional e Estrutura de Dados Eficiente (Busca Hash)
* Arquitetura de APIs com Chaves de Idempotência
* Manipulação Dinâmica de Arquivos JSON (Leitura Assíncrona)
* Desenvolvimento Full-Stack Independente Otimizado para Mobile
