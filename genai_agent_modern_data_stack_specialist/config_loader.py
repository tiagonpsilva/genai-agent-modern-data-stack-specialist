import os
import yaml
from .config_models import Settings
from pydantic import ValidationError

class ConfigLoaderError(Exception):
    pass

def _env_var_constructor(loader, node):
    value = loader.construct_scalar(node)
    if value.startswith('${') and value.endswith('}'):
        env_var = value[2:-1]
        env_value = os.getenv(env_var)
        if env_value is None:
            raise ConfigLoaderError(f"Variável de ambiente obrigatória não definida: {env_var}")
        return env_value
    return value

yaml.add_implicit_resolver('!env_var', r'\$\{[^}]+\}', None)
yaml.add_constructor('!env_var', _env_var_constructor)

def load_settings(config_path: str = "config.yaml") -> Settings:
    """
    Carrega as configurações do agente a partir de um arquivo YAML.
    Substitui variáveis de ambiente no formato ${VARIAVEL} automaticamente.
    Lança erro se variável obrigatória não estiver definida.

    Exemplo de uso:
        from genai_agent_modern_data_stack_specialist.config_loader import load_settings
        settings = load_settings()
        print(settings.llm.model_name)
    """
    with open(config_path, "r") as f:
        raw = f.read()
    # Substitui variáveis de ambiente manualmente
    import re
    def replace_env_var(match):
        env_var = match.group(1)
        env_value = os.getenv(env_var)
        if env_value is None:
            raise ConfigLoaderError(f"Variável de ambiente obrigatória não definida: {env_var}")
        return env_value
    raw = re.sub(r'\$\{([^}]+)\}', replace_env_var, raw)
    data = yaml.safe_load(raw)
    try:
        return Settings(**data)
    except ValidationError as e:
        raise ConfigLoaderError(f"Erro de validação na configuração: {e}") 