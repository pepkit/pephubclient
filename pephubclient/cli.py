import typer

from pephubclient import __app_name__, __version__
from pephubclient.pephubclient import PEPHubClient
from github_oauth_client.github_oauth_client import GitHubOAuthClient

pep_hub_client = PEPHubClient()
github_client = GitHubOAuthClient()
app = typer.Typer()


@app.command()
def pull(project_query_string: str):
    pep_hub_client.save_pep_locally(project_query_string)


@app.command()
def login():
    github_client.login()
    print(github_client.access_token)


@app.command()
def version():
    print(f"{__app_name__} v{__version__}")
