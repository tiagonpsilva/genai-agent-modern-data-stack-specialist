# 🤖 Agente Especialista em Modern Data Stack

![Python](https://img.shields.io/badge/language-Python-blue?logo=python) ![Python Version](https://img.shields.io/badge/python-3.8%2B-blue) ![Typer](https://img.shields.io/badge/CLI-Typer-0b7fab?logo=python) ![Langchain](https://img.shields.io/badge/LLM-Langchain-ffb86b) ![UI Rich](https://img.shields.io/badge/UI-Rich-6e44ff) ![Pydantic](https://img.shields.io/badge/config-Pydantic-009688?logo=pydantic) ![Poetry](https://img.shields.io/badge/build-poetry-60b5cc?logo=poetry)

## 📦 Sobre o Projeto
Agente de linha de comando (CLI) que analisa até 5 repositórios locais do Github e responde, em português, sobre objetivo, detalhes e estrutura dos projetos, com foco em modern data stack.

## 📁 Estrutura Inicial 

```bash
.
├── genai_agent_langchain_sample/
│   ├── __init__.py
│   └── cli.py
├── README.md
├── pyproject.toml
├── .gitignore
```

## 🚀 Como executar 

1. Instale o Poetry (se ainda não tiver):
   ```bash
   pip install poetry
   ```
2. Instale as dependências do projeto:
   ```bash
   poetry install
   ```
3. Ative o ambiente virtual:
   ```bash
   poetry shell
   ```
4. Execute o CLI:
   ```bash
   genai-agent
   ```
   Ao rodar apenas `genai-agent`, você verá uma mensagem de boas-vindas e o help com todos os comandos disponíveis, sem erro.

   Para iniciar o modo interativo:
   ```bash
   genai-agent interativo
   ```
   Ou rode diretamente:
   ```bash
   python -m genai_agent_langchain_sample.cli
   ```

---

## 🧩 Architecture Haiku

Pergunte ao agente  
Chroma e embeddings servem  
Resposta contextual

### 📝 Descrição breve do sistema
Um agente de linha de comando (CLI), especialista em "modern data stack", que analisa até 5 repositórios locais do Github, ignora arquivos irrelevantes (como os listados em .gitignore) e responde, em português, sobre o objetivo, detalhes e estrutura dos projetos, apresentando-se como especialista no tema, exibindo mensagem de boas-vindas personalizada e suportando comandos interativos e de ajuda.

### 🎯 Principais objetivos de negócio
- Permitir consultas em português sobre propósito, detalhes e estrutura de até 5 repositórios locais via CLI.
- Oferecer respostas especializadas e contextualizadas sobre "modern data stack".
- Facilitar a apresentação do agente como especialista, adaptando sua introdução ao domínio e aos repositórios analisados.
- Sugerir perguntas e exemplos de uso ao iniciar, promovendo engajamento e facilidade de uso.
- Suportar comandos interativos e comando de ajuda detalhado.

### ⛔ Principais restrições identificadas
- Suporte exclusivo ao idioma português.
- Limite de até 5 repositórios por consulta.
- Análise apenas de arquivos relevantes, ignorando os listados em .gitignore e outros irrelevantes.
- Operação apenas em ambiente local (sem integração online inicial).
- Interface apenas via CLI.
- Não há persistência de dados, logs, exportação de respostas ou suporte a múltiplos usuários.

### 🏆 Prioridade dos atributos de qualidade
Simplicidade > Especialização > Usabilidade > Flexibilidade

### 🛠️ Principais decisões de design
- CLI como interface única, com banner de boas-vindas, sugestões de perguntas ao iniciar, modo interativo e comando de ajuda.
- Especialização fixa em "modern data stack", com apresentação personalizada.
- Uso do Langchain para processamento de linguagem natural e geração de respostas especializadas.
- Uso do Pydantic para modelagem, validação e documentação das configurações do agente.
- Análise completa dos repositórios locais, ignorando arquivos irrelevantes conforme .gitignore e regras adicionais.
- Estrutura modular para futura expansão (ex: suporte online, logs, múltiplos domínios).

### 👥 Ponderações críticas dos especialistas

**[Arquiteto de Integração]**
A especialização fixa simplifica o onboarding e garante foco. Ignorar arquivos irrelevantes é essencial para performance e qualidade das respostas.  
Nota: 10

**[Arquiteto de Dados]**
Foco em arquivos relevantes garante contexto de qualidade. Especialização em modern data stack é aderente ao mercado atual.  
Nota: 10

**[Arquiteto de Nuvem]**
Processamento local e sem dependências externas mantém o custo zero e facilita adoção.  
Nota: 10

**[Arquiteto de Segurança]**
Ignorar arquivos sensíveis e irrelevantes reduz riscos. Sem logs ou exportação, privacidade é garantida.  
Nota: 10

**[Arquiteto de Infraestrutura]**
Instalação local simples, dependências devem ser bem documentadas.  
Nota: 10

**[Designer de Negócios]**
Experiência interativa e especialização clara entregam valor imediato e diferencial competitivo.  
Nota: 10

**Média geral:** 10 