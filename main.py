import sys
from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table

from manifest_parser import parse_manifest
from license_agent import check_compliance

app = typer.Typer(help="RepoGuardian License Auditor")
console = Console()

@app.command(name="audit")
def audit(path: str):
    """Audits compliance of packages in the given manifest file."""
    try:
        packages = parse_manifest(path)
    except Exception as e:
        console.print(f"[bold red]Error reading manifest:[/bold red] {e}")
        raise typer.Exit(code=1)

    results = check_compliance(packages, policy_path="policy.json")

    table = Table(title="License Compliance Summary")
    table.add_column("Package", style="cyan")
    table.add_column("Version", style="magenta")
    table.add_column("License", style="blue")
    table.add_column("Status", style="bold")
    table.add_column("Citation", style="italic")

    has_denied = False

    for item in results:
        status = item["status"]
        if status == "allowed":
            status_style = "[green]allowed[/green]"
        elif status == "warning":
            status_style = "[yellow]warning[/yellow]"
        elif status == "denied":
            status_style = "[red]denied[/red]"
            has_denied = True
        else:
            status_style = "[bright_black]unknown[/bright_black]"

        table.add_row(
            item["package"],
            item["version"],
            item["license"],
            status_style,
            item["citation"]
        )

    console.print(table)

    with open("AUDIT_REPORT.md", "w") as f:
        f.write("# License Audit Report\n\n")
        f.write("| Package | Version | License | Status | Citation |\n")
        f.write("|---|---|---|---|---|\n")
        for item in results:
            f.write(f"| {item['package']} | {item['version']} | {item['license']} | {item['status']} | {item['citation']} |\n")

    if has_denied:
        raise typer.Exit(code=1)
    else:
        raise typer.Exit(code=0)

@app.command(name="version")
def version():
    """Prints tool version."""
    console.print("RepoGuardian v1.0.0")

if __name__ == "__main__":
    app()