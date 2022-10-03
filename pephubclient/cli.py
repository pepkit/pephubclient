import typer

from pephubclient import __app_name__, __version__
from pephubclient.pephubclient import PEPHubClient

pep_hub_client = PEPHubClient()
app = typer.Typer()


@app.command()
def pull(project_query_string: str):
    pep_hub_client.save_pep_locally(project_query_string)


@app.command()
def login():
    print("Logging in...")


@app.command()
def version():
    print(f"{__app_name__} v{__version__}")
