# 📍 Roadmap do Projeto

Este diretório contém o planejamento evolutivo (roadmap) do agente especialista em Modern Data Stack. Cada arquivo detalha uma etapa representativa do desenvolvimento, com objetivos, tarefas (to-dos) e observações.

## 🗺️ Visão Geral — Diagrama C4 (Contexto)

```mermaid
%%{init: { "themeVariables": { "fontFamily": "Arial", "fontSize": "10px" } }}%%
C4Context
    title Agente Especialista em Modern Data Stack
    Person(user, "Usuário", "Interage via CLI para consultar repositórios e obter respostas especializadas.")
    System(agent, "Agente CLI Modern Data Stack", "Processa perguntas, analisa repositórios e responde usando LLM.")
    System_Ext(github, "GitHub", "Fonte dos repositórios locais")
    System_Ext(llm, "LLM/Embeddings", "Modelo de linguagem e embeddings para análise semântica")
    user -> agent: Perguntas e comandos
    agent -> github: Lê repositórios locais
    agent -> llm: Consulta LLM/embeddings para gerar respostas
```

## Etapas

- [01 - CLI Básico](01-cli-basico.md)
- [02 - Configuração da LLM e Embeddings](02-configuracao-llm-embeddings.md)
- [03 - Configuração dos Repositórios do Github](03-configuracao-repositorios.md)
- [04 - Configuração Geral e Variáveis de Ambiente](04-configuracao-geral-e-variaveis.md)
- [05 - Prompt Base e Características do Agente](05-prompt-base-e-caracteristicas.md)
- [06 - Integração e Orquestração Final](06-integracao-e-orquestracao.md)

Sinta-se à vontade para sugerir novas etapas ou abrir issues para discussões! 