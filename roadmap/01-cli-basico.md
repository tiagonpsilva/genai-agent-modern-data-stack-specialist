# CLI Básico

![Status](https://img.shields.io/badge/status-concluído-brightgreen)

## Objetivo
Implementar a estrutura inicial do CLI, com comando principal, mensagem de boas-vindas e modo interativo (esqueleto).

## 🗂️ Diagrama de Sequência — Fluxo Básico

```mermaid
%%{init: { "themeVariables": { "fontFamily": "Arial", "fontSize": "10px" } }}%%
sequenceDiagram
    participant U as Usuário
    participant CLI as CLI
    U->>CLI: Executa comando (ex: genai-agent interativo)
    CLI->>CLI: Exibe mensagem de boas-vindas
    CLI->>U: Mostra opções/comandos
    U->>CLI: Seleciona comando/interage
    CLI->>CLI: Processa entrada
    CLI->>U: Exibe resposta ou inicia modo interativo
```

## Tarefas (To-Do)
- [x] Estrutura de pacote Python recomendada
- [x] Comando principal `genai-agent` com mensagem amigável
- [x] Comando `interativo` (esqueleto)
- [x] Mensagem de boas-vindas e help automático
- [x] README com instruções e badges

## Observações
- O CLI deve ser fácil de instalar e executar.
- O modo interativo será expandido nas próximas etapas. 