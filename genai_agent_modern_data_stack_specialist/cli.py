import typer
from rich.console import Console
from rich.panel import Panel
import sys
from .config_loader import load_settings, ConfigLoaderError
from .repo_utils import aggregate_repo_data
import openai
import json
import os
import glob

def safe_model_dump(settings):
    def mask_secrets(obj):
        if isinstance(obj, dict):
            return {k: (mask_secrets(v)) for k, v in obj.items()}
        elif hasattr(obj, "get_secret_value"):
            return "***"
        elif isinstance(obj, list):
            return [mask_secrets(i) for i in obj]
        return obj
    return mask_secrets(settings.model_dump())

PERSONA_DIR = "prompts/personas"

app = typer.Typer()
console = Console()

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Agente especialista em Modern Data Stack. Analisa até 5 repositórios locais e responde perguntas sobre objetivo, detalhes e estrutura dos projetos."""
    if ctx.invoked_subcommand is None:
        console.print(Panel("Bem-vindo ao Agente Modern Data Stack!", title="Modern Data Stack", subtitle="Powered by Langchain", expand=False))
        console.print("[bold green]Digite [yellow]genai-agent interativo[/yellow] para iniciar o modo de perguntas interativas![/bold green]")
        console.print("[bold green]Ou use [yellow]genai-agent --help[/yellow] para ver todos os comandos disponíveis.[/bold green]")
        help_text = ctx.get_help()
        console.print(help_text)
        sys.exit(0)

@app.command()
def interativo(
    persona: str = typer.Option(..., help="Nome da persona (ex: arquiteto-dados, engenheiro-dados). Será buscado em prompts/personas/<nome>.md"),
    config: str = typer.Option("config.yaml", help="Caminho para o arquivo de configuração YAML."),
    llm_provider: str = typer.Option(None, help="Sobrescreve o provedor da LLM."),
    llm_model: str = typer.Option(None, help="Sobrescreve o modelo da LLM."),
    llm_temperature: float = typer.Option(None, help="Sobrescreve a temperatura da LLM."),
    emb_provider: str = typer.Option(None, help="Sobrescreve o provedor de embeddings."),
    emb_model: str = typer.Option(None, help="Sobrescreve o modelo de embeddings.")
):
    """Inicia o modo interativo para perguntas sobre os repositórios, exigindo seleção de persona."""
    try:
        settings = load_settings(config)
    except ConfigLoaderError as e:
        console.print(f"[bold red]Erro ao carregar configuração:[/bold red] {e}")
        raise typer.Exit(1)

    # Sobrescreve parâmetros se fornecidos
    if llm_provider:
        settings.llm.provider = llm_provider
    if llm_model:
        settings.llm.model_name = llm_model
    if llm_temperature is not None:
        settings.llm.temperature = llm_temperature
    if emb_provider:
        settings.embeddings.provider = emb_provider
    if emb_model:
        settings.embeddings.model_name = emb_model

    # Exibe configuração mascarando segredos
    console.print(Panel(
        f"Modo interativo iniciado!\n\n[bold]Configuração carregada:[/bold]\n[green]{json.dumps(safe_model_dump(settings), indent=2, ensure_ascii=False)}[/green]",
        title="Interativo", expand=False))

    # Monta caminho do arquivo de persona
    persona_path = os.path.join(PERSONA_DIR, f"{persona}.md")
    if not os.path.isfile(persona_path):
        console.print(f"[bold red]Arquivo de persona não encontrado:[/bold red] {persona_path}")
        raise typer.Exit(1)
    try:
        with open(persona_path, "r", encoding="utf-8") as f:
            prompt_base = f.read()
    except Exception as e:
        console.print(f"[bold red]Erro ao carregar persona:[/bold red] {e}")
        raise typer.Exit(1)

    # Agrega contexto do primeiro repositório habilitado
    repo = next((r for r in settings.repos if r.enabled), None)
    if not repo:
        console.print("[bold yellow]Nenhum repositório habilitado encontrado na configuração.[/bold yellow]")
        raise typer.Exit(1)
    contexto = aggregate_repo_data(repo.path)

    openai.api_key = settings.llm.api_key.get_secret_value()

    while True:
        pergunta = console.input("[bold cyan]Digite sua pergunta (ou 'sair' para encerrar): [/bold cyan]").strip()
        if pergunta.lower() in ("sair", "exit"): 
            console.print("[bold green]Sessão encerrada. Até logo![/bold green]")
            break
        # Monta o prompt
        prompt = prompt_base.replace("{contexto_repositorio}", contexto).replace("{pergunta_usuario}", pergunta)
        try:
            response = openai.chat.completions.create(
                model=settings.llm.model_name,
                messages=[{"role": "system", "content": "Você é um especialista em Modern Data Stack."},
                          {"role": "user", "content": prompt}],
                temperature=settings.llm.temperature,
                max_tokens=500
            )
            resposta = response.choices[0].message.content.strip()
            console.print(Panel(f"[bold]Resposta da LLM:[/bold]\n\n{resposta}", title="OpenAI LLM", expand=False))
        except Exception as e:
            console.print(f"[bold red]Erro ao consultar a LLM:[/bold red] {e}")

@app.command()
def testar_llm(
    config: str = typer.Option("config.yaml", help="Caminho para o arquivo de configuração YAML."),
):
    """Testa a integração com a LLM da OpenAI usando o primeiro repositório habilitado."""
    try:
        settings = load_settings(config)
    except ConfigLoaderError as e:
        console.print(f"[bold red]Erro ao carregar configuração:[/bold red] {e}")
        raise typer.Exit(1)

    repo = next((r for r in settings.repos if r.enabled), None)
    if not repo:
        console.print("[bold yellow]Nenhum repositório habilitado encontrado na configuração.[/bold yellow]")
        raise typer.Exit(1)

    console.print(f"[bold]Agregando dados do repositório:[/bold] {repo.name} ({repo.path})")
    conteudo = aggregate_repo_data(repo.path)
    prompt = (
        "Resuma o objetivo deste repositório em 3 frases.\n"
        "Abaixo está o conteúdo relevante:\n\n"
        f"{conteudo}"
    )

    openai.api_key = settings.llm.api_key.get_secret_value()
    try:
        response = openai.chat.completions.create(
            model=settings.llm.model_name,
            messages=[{"role": "system", "content": "Você é um especialista em Modern Data Stack."},
                      {"role": "user", "content": prompt}],
            temperature=settings.llm.temperature,
            max_tokens=300
        )
        resposta = response.choices[0].message.content.strip()
        console.print(Panel(f"[bold]Resposta da LLM:[/bold]\n\n{resposta}", title="OpenAI LLM", expand=False))
    except Exception as e:
        console.print(f"[bold red]Erro ao consultar a LLM:[/bold red] {e}")
        raise typer.Exit(1)

@app.command()
def listar_personas():
    """Lista todas as personas disponíveis em prompts/personas/"""
    persona_files = glob.glob(os.path.join(PERSONA_DIR, '*.md'))
    if not persona_files:
        console.print("[bold yellow]Nenhuma persona encontrada em prompts/personas/.[/bold yellow]")
        return
    console.print("[bold green]Personas disponíveis:[/bold green]")
    for pf in persona_files:
        nome = os.path.splitext(os.path.basename(pf))[0]
        console.print(f"- {nome}")

@app.command()
def debate(
    persona1: str = typer.Option(..., help="Nome da primeira persona (ex: arquiteto-dados)"),
    persona2: str = typer.Option(..., help="Nome da segunda persona (ex: engenheiro-dados)"),
    config: str = typer.Option("config.yaml", help="Caminho para o arquivo de configuração YAML."),
    max_tokens: int = typer.Option(500, help="Limite de tokens por resposta")
):
    """Executa um mini-debate entre duas personas sobre uma pergunta do usuário."""
    # Carrega configuração
    try:
        settings = load_settings(config)
    except ConfigLoaderError as e:
        console.print(f"[bold red]Erro ao carregar configuração:[/bold red] {e}")
        raise typer.Exit(1)

    # Monta caminhos dos arquivos de persona
    persona_path1 = os.path.join(PERSONA_DIR, f"{persona1}.md")
    persona_path2 = os.path.join(PERSONA_DIR, f"{persona2}.md")
    if not os.path.isfile(persona_path1):
        console.print(f"[bold red]Arquivo de persona não encontrado:[/bold red] {persona_path1}")
        raise typer.Exit(1)
    if not os.path.isfile(persona_path2):
        console.print(f"[bold red]Arquivo de persona não encontrado:[/bold red] {persona_path2}")
        raise typer.Exit(1)
    with open(persona_path1, "r", encoding="utf-8") as f:
        prompt_base1 = f.read()
    with open(persona_path2, "r", encoding="utf-8") as f:
        prompt_base2 = f.read()

    # Agrega contexto do primeiro repositório habilitado
    repo = next((r for r in settings.repos if r.enabled), None)
    if not repo:
        console.print("[bold yellow]Nenhum repositório habilitado encontrado na configuração.[/bold yellow]")
        raise typer.Exit(1)
    contexto = aggregate_repo_data(repo.path)

    openai.api_key = settings.llm.api_key.get_secret_value()

    pergunta = console.input("[bold cyan]Digite a pergunta para o debate (ou 'sair' para encerrar): [/bold cyan]").strip()
    if pergunta.lower() in ("sair", "exit"):
        console.print("[bold green]Debate cancelado. Até logo![/bold green]")
        raise typer.Exit(0)

    # 1. Persona 1 responde normalmente
    prompt1 = prompt_base1.replace("{contexto_repositorio}", contexto).replace("{pergunta_usuario}", pergunta)
    try:
        resp1 = openai.chat.completions.create(
            model=settings.llm.model_name,
            messages=[{"role": "system", "content": "Você é um especialista em Modern Data Stack."},
                      {"role": "user", "content": prompt1}],
            temperature=settings.llm.temperature,
            max_tokens=max_tokens
        ).choices[0].message.content.strip()
    except Exception as e:
        console.print(f"[bold red]Erro ao consultar a LLM para {persona1}:[/bold red] {e}")
        raise typer.Exit(1)

    # 2. Persona 2 complementa/contrapõe, usando resposta da Persona 1 como contexto
    prompt2 = (
        prompt_base2.replace("{contexto_repositorio}", contexto)
        .replace("{pergunta_usuario}", f"{pergunta}\n\nResposta anterior ({persona1}):\n{resp1}")
    )
    try:
        resp2 = openai.chat.completions.create(
            model=settings.llm.model_name,
            messages=[{"role": "system", "content": "Você é um especialista em Modern Data Stack."},
                      {"role": "user", "content": prompt2}],
            temperature=settings.llm.temperature,
            max_tokens=max_tokens
        ).choices[0].message.content.strip()
    except Exception as e:
        console.print(f"[bold red]Erro ao consultar a LLM para {persona2}:[/bold red] {e}")
        raise typer.Exit(1)

    # 3. Persona 1 faz réplica, usando resposta da Persona 2 como contexto
    prompt1_replica = (
        prompt_base1.replace("{contexto_repositorio}", contexto)
        .replace("{pergunta_usuario}", f"{pergunta}\n\nResposta anterior ({persona2}):\n{resp2}")
    )
    try:
        resp1_replica = openai.chat.completions.create(
            model=settings.llm.model_name,
            messages=[{"role": "system", "content": "Você é um especialista em Modern Data Stack."},
                      {"role": "user", "content": prompt1_replica}],
            temperature=settings.llm.temperature,
            max_tokens=max_tokens
        ).choices[0].message.content.strip()
    except Exception as e:
        console.print(f"[bold red]Erro ao consultar a LLM para réplica de {persona1}:[/bold red] {e}")
        raise typer.Exit(1)

    # Exibe o debate formatado
    console.print(Panel(f"[bold]{persona1.replace('-', ' ').title()}[/bold]:\n{resp1}", title=f"{persona1}", expand=False))
    console.print(Panel(f"[bold]{persona2.replace('-', ' ').title()}[/bold] (comentando {persona1}):\n{resp2}", title=f"{persona2}", expand=False))
    console.print(Panel(f"[bold]{persona1.replace('-', ' ').title()}[/bold] (réplica):\n{resp1_replica}", title=f"{persona1} (réplica)", expand=False))

if __name__ == "__main__":
    app() 