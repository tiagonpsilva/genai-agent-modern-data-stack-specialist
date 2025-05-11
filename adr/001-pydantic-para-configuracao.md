# 📝 ADR 001: Uso do Pydantic para Configuração e Validação

## 📌 Contexto
O agente precisa lidar com múltiplos arquivos de configuração (LLM, embeddings, repositórios, prompt base, variáveis de ambiente) e garantir segurança, flexibilidade e validação automática dos dados.

## 💡 Decisão Tomada
Adotar a biblioteca [Pydantic](https://docs.pydantic.dev/) para modelar, validar e documentar todas as configurações do agente.

## 🎯 Justificativas
- Validação automática de tipos e campos obrigatórios.
- Conversão automática de tipos (ex: str para int, etc).
- Facilidade para documentar e expandir modelos de configuração.
- Integração nativa com variáveis de ambiente (via pydantic-settings).
- Segurança para dados sensíveis (ex: uso de SecretStr).
- Melhora a legibilidade, manutenção e testabilidade do código.

## 🚦 Alternativas Consideradas
- Usar apenas dicionários Python e validação manual.
- Usar dataclasses padrão do Python.
- Usar outras libs (ex: Marshmallow, Cerberus), mas Pydantic é mais moderno e integrado ao ecossistema atual.

## 🛤️ Consequências
- O projeto ganha robustez e clareza na manipulação de configurações.
- Facilita a evolução futura (novos campos, validações, integrações).
- Pequena dependência extra, mas com grande benefício para qualidade do código. 