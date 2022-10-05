import typer
from github_oauth_client.github_oauth_client import GitHubOAuthClient
from pephubclient import __app_name__, __version__
from pephubclient.pephubclient import PEPHubClient
from pephubclient.models import ClientData


GITHUB_CLIENT_ID = "20a452cc59b908235e50"


pep_hub_client = PEPHubClient()
github_client = GitHubOAuthClient()
app = typer.Typer()
client_data = ClientData(client_id=GITHUB_CLIENT_ID)


@app.command()
def login():
    pep_hub_client.login(client_data)


@app.command()
def logout():
    pep_hub_client.logout()


@app.command()
def pull(project_query_string: str):
    pep_hub_client.pull(project_query_string)


@app.command()
def version():
    print(f"{__app_name__} v{__version__}")
