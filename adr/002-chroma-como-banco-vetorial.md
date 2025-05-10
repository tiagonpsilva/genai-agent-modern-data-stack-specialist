# 🗃️ ADR 002: Uso do Chroma como Banco de Dados Vetorial

## 📄 Contexto
O agente CLI especialista em Modern Data Stack precisa de uma solução eficiente para persistência e busca semântica de embeddings, permitindo consultas rápidas sobre múltiplos repositórios de código.

## ✅ Decisão
Adotar o **Chroma** como banco de dados vetorial principal para persistência e busca de embeddings.

## 💡 Alternativas Consideradas
- **FAISS**: Muito rápido, mas menos amigável para persistência e integração local.
- **Pinecone**: SaaS robusto, mas depende de serviço externo e custos.
- **Weaviate, Milvus, Qdrant**: Escaláveis, mas mais complexos para setup local.
- **Chroma**: Open source, fácil de instalar, integração nativa com Langchain, persistência local simples.

## 📝 Motivação
- Permite prototipagem local e escalabilidade futura.
- Integração direta com Langchain e Python.
- Persistência local sem dependências externas.
- Comunidade ativa e documentação clara.

## 🔗 Impacto
- O fluxo de embeddings e busca semântica será centralizado no Chroma.
- Facilita evolução futura para outros bancos vetoriais, se necessário.

## 🏁 Status
**Aprovado e implementado no roadmap como etapa dedicada.** 