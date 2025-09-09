# cli/accelerator_cli.py
import typer
import shutil
from pathlib import Path

app = typer.Typer(help="🚀 Accelerator CLI - Create projects with optional modules")

BASE_TEMPLATES = Path(__file__).resolve().parent.parent / "templates"

@app.command()
def create_project(name: str, with_: str = typer.Option("", "--with", help="Comma-separated list of modules to include")):
    """
    Create a new project from the accelerator templates.
    Example:
        accelerator-cli create-project my-saas --with frontend,payments,assistants
    """
    project_path = Path(name)
    if project_path.exists():
        typer.echo(f"❌ Project folder '{name}' already exists.")
        raise typer.Exit(1)

    typer.echo(f"📂 Creating project '{name}'...")
    project_path.mkdir()

    # Copy core & shared always
    for folder in ["core_backend", "shared"]:
        src = BASE_TEMPLATES / folder
        dst = project_path / folder
        shutil.copytree(src, dst)
        typer.echo(f"   ✅ Added {folder}")

    # Copy optional modules
    modules = [m.strip() for m in with_.split(",") if m.strip()]
    for module in modules:
        src = BASE_TEMPLATES / module
        dst = project_path / "modules" / module
        if not src.exists():
            typer.echo(f"   ⚠️  Skipping unknown module '{module}'")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dst)
        typer.echo(f"   ✅ Added module {module}")

    typer.echo(f"\n🚀 Project '{name}' created successfully with modules: {modules}")


if __name__ == "__main__":
    app()
