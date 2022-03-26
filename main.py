import sys
import typer

from src.utils.changelog import generate_changelog

app = typer.Typer()



@app.command(name='changelog')
def changelog(stdin = sys.stdin):
    changelog = generate_changelog(stdin.readlines)
    typer.echo(changelog)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
