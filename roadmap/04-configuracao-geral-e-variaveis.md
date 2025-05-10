# Configuração Geral e Variáveis de Ambiente

## Objetivo
Criar uma estrutura centralizada para configurações do agente, incluindo o uso de variáveis de ambiente para manter credenciais e dados sensíveis seguros.

## 🗺️ Diagrama C4 — Configuração Centralizada

```mermaid
%%{init: { "themeVariables": { "fontFamily": "Arial", "fontSize": "10px" } }}%%
C4Container
    title Configuração Centralizada
    Person(user, "Usuário")
    Container(agent, "Agente CLI", "Python/Typer")
    Container(config, "Arquivo de Configuração", "config.yaml/.env")
    user -> agent: Define/atualiza configurações
    agent -> config: Lê variáveis e credenciais
```

## Tarefas (To-Do)
- [ ] Definir formato e local do arquivo de configuração principal (ex: config.yaml, .env)
- [ ] Implementar leitura de variáveis de ambiente para credenciais (ex: tokens de API)
- [ ] Documentar variáveis obrigatórias e opcionais
- [ ] Garantir que dados sensíveis não sejam versionados (atualizar .gitignore)

## Observações
- O uso de variáveis de ambiente é fundamental para segurança.
- A configuração deve ser clara e fácil de modificar. 