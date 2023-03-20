import typer
from pephubclient import __app_name__, __version__
from pephubclient.pephubclient import PEPHubClient

pep_hub_client = PEPHubClient()

app = typer.Typer()

@app.command()
def login():
    pep_hub_client.login()


@app.command()
def logout():
    pep_hub_client.logout()


@app.command()
def pull(project_query_string: str):
    pep_hub_client.pull(project_query_string)


@app.command()
def version():
    print(f"{__app_name__} v{__version__}")
