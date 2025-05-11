import os
from pathlib import Path
from typing import List

def aggregate_repo_data(repo_path: str) -> str:
    """
    Agrega dados relevantes de um repositório local para análise por LLM.
    - Lê o conteúdo do README.md (se existir)
    - Lê até 5 arquivos .py mais relevantes (maiores por tamanho)
    - Retorna uma string única, separando cada seção
    """
    repo = Path(repo_path)
    partes: List[str] = []

    # Adiciona README.md
    readme = repo / "README.md"
    if readme.exists():
        partes.append(f"# README.md\n\n{readme.read_text(encoding='utf-8', errors='ignore')}\n")

    # Seleciona até 5 arquivos .py maiores
    py_files = sorted(repo.rglob("*.py"), key=lambda f: f.stat().st_size, reverse=True)[:5]
    for py_file in py_files:
        partes.append(f"# {py_file.relative_to(repo)}\n\n{py_file.read_text(encoding='utf-8', errors='ignore')}\n")

    if not partes:
        partes.append("(Nenhum dado relevante encontrado no repositório)")
    return "\n\n".join(partes) 