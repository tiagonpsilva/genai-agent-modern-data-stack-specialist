from pydantic import BaseModel, Field, SecretStr
from typing import List, Optional

class LLMConfig(BaseModel):
    provider: str = Field(..., description="Nome do provedor da LLM, ex: openai")
    api_key: SecretStr = Field(..., description="Chave de API para acesso à LLM (OpenAI)")
    model_name: str = Field(..., description="Nome do modelo a ser utilizado (ex: gpt-3.5-turbo)")
    temperature: float = Field(0.7, description="Temperatura do modelo para geração de respostas")

class EmbeddingsConfig(BaseModel):
    provider: str = Field(..., description="Provedor dos embeddings, ex: openai")
    model_name: str = Field(..., description="Nome do modelo de embeddings (ex: text-embedding-3-small)")
    api_key: Optional[SecretStr] = Field(None, description="Chave de API para embeddings, se necessário (OpenAI)")

class RepoConfig(BaseModel):
    name: str = Field(..., description="Nome identificador do repositório")
    path: str = Field(..., description="Caminho local do repositório")
    enabled: bool = Field(True, description="Se o repositório está ativo para análise")

class PromptConfig(BaseModel):
    path: str = Field(..., description="Caminho para o arquivo do prompt base")
    description: Optional[str] = Field(None, description="Descrição ou persona do agente")

class Settings(BaseModel):
    llm: LLMConfig
    embeddings: EmbeddingsConfig
    repos: List[RepoConfig]
    prompt: PromptConfig 