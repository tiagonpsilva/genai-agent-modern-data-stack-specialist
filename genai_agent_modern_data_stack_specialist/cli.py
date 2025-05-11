import typer
from rich.console import Console
from rich.panel import Panel
import sys
from .config_loader import load_settings, ConfigLoaderError
from .repo_utils import aggregate_repo_data
import openai
import json

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
    config: str = typer.Option("config.yaml", help="Caminho para o arquivo de configuração YAML."),
    llm_provider: str = typer.Option(None, help="Sobrescreve o provedor da LLM."),
    llm_model: str = typer.Option(None, help="Sobrescreve o modelo da LLM."),
    llm_temperature: float = typer.Option(None, help="Sobrescreve a temperatura da LLM."),
    emb_provider: str = typer.Option(None, help="Sobrescreve o provedor de embeddings."),
    emb_model: str = typer.Option(None, help="Sobrescreve o modelo de embeddings.")
):
    """Inicia o modo interativo para perguntas sobre os repositórios."""
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

    # Carrega prompt-base
    try:
        with open(settings.prompt.path, "r", encoding="utf-8") as f:
            prompt_base = f.read()
    except Exception as e:
        console.print(f"[bold red]Erro ao carregar prompt-base:[/bold red] {e}")
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

if __name__ == "__main__":
    app() 