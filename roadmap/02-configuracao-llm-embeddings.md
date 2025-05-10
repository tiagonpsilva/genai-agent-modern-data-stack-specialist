# Configuração da LLM e Embeddings

## 🗺️ Diagrama C4 — LLM e Embeddings

```mermaid
%%{init: { "themeVariables": { "fontFamily": "Arial", "fontSize": "10px" } }}%%
C4Container
    title Configuração LLM e Embeddings
    Person(user, "Usuário")
    Container(agent, "Agente CLI", "Python/Typer")
    Container(llm, "LLM", "OpenAI/HuggingFace")
    Container(emb, "Embeddings", "OpenAI/Sentence Transformers")
    user -> agent: Perguntas
    agent -> llm: Consulta modelo de linguagem
    agent -> emb: Gera/consulta embeddings
```

## Objetivo
Configurar o modelo de linguagem (LLM) a ser utilizado pelo agente, bem como a estrutura de embeddings para análise semântica dos repositórios.

## Tarefas (To-Do)
- [ ] Definir e integrar a LLM (ex: OpenAI, HuggingFace, etc)
- [ ] Configurar provedores e parâmetros da LLM via arquivo de configuração
- [ ] Implementar estrutura de embeddings para análise semântica
- [ ] Permitir troca fácil de modelo/embeddings via configuração
- [ ] Documentar opções e exemplos de configuração

## Observações
- A escolha da LLM e embeddings deve ser flexível e segura.
- O agente deve ser capaz de operar com diferentes provedores/modelos. 