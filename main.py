import sys
import typer

from src.utils.changelog import generate_changelog
from src.utils.deployment import generate_deployment_notes

app = typer.Typer()



@app.command(name='changelog')
def changelog(include_details: bool = True):
    changelog = generate_changelog(sys.stdin.readlines, include_details=include_details)
    typer.echo(changelog)


@app.command(name='deployment-note')
def changelog():
    deployment_notes = generate_deployment_notes(sys.stdin.readlines)
    typer.echo(deployment_notes)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
