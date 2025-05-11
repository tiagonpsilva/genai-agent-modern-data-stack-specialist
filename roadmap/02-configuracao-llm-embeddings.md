# Configuração da LLM e Embeddings

![Status](https://img.shields.io/badge/status-concluído-brightgreen)

## 🗺️ Diagrama de Containers — LLM e Embeddings

```mermaid
%%{init: { "themeVariables": { "fontFamily": "Arial", "fontSize": "10px" } }}%%
flowchart TD
    U[Usuário]
    CLI[Agente CLI - Python Typer]
    LLM[LLM - OpenAI/HuggingFace]
    EMB[Embeddings - OpenAI/Sentence Transformers]
    U -->|Perguntas| CLI
    CLI -->|Consulta modelo de linguagem| LLM
    CLI -->|Gera/consulta embeddings| EMB
```

## Objetivo
Configurar o modelo de linguagem (LLM) a ser utilizado pelo agente, bem como a estrutura de embeddings para análise semântica dos repositórios.

## Tarefas (To-Do)
- [x] Definir e integrar a LLM (ex: OpenAI, HuggingFace, etc)
- [x] Configurar provedores e parâmetros da LLM via arquivo de configuração
- [x] Implementar estrutura de embeddings para análise semântica
- [x] Permitir troca fácil de modelo/embeddings via configuração
- [x] Documentar opções e exemplos de configuração

## Observações
- A escolha da LLM e embeddings deve ser flexível e segura.
- O agente deve ser capaz de operar com diferentes provedores/modelos. 