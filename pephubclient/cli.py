import typer
from pephubclient import __app_name__, __version__
from pephubclient.pephubclient import PEPHubClient

pep_hub_client = PEPHubClient()

app = typer.Typer()


@app.command()
def login():
    """
    Login to Pephub
    """
    pep_hub_client.login()


@app.command()
def logout():
    """
    Logout
    """
    pep_hub_client.logout()


@app.command()
def pull(
    project_registry_path: str,
    # output_dir: str = typer.Option(None, help="Specify the location where the file should be saved"),
    project_format: str = typer.Option("default", help="Project format in which project should be saved"
                                                       "Options: [default, basic, csv, yaml, zip]."),
    force: bool = typer.Option(False, help="Last name of person to greet."),
):
    """
    Download and save project locally.
    """
    pep_hub_client.pull(project_registry_path, project_format, force)



@app.command()
def push(
    cfg: str = typer.Option(
        ...,
        help="Project config file (YAML) or sample table (CSV/TSV)"
        "with one row per sample to constitute project",
    ),
    namespace: str = typer.Option(..., help="Project name"),
    name: str = typer.Option(..., help="Project name"),
    tag: str = typer.Option(None, help="Project tag"),
    force: bool = typer.Option(
        False, help="Force push to the database. Use it to update, or upload project."
    ),
):
    """
    Upload/update project in PEPhub
    """
    ...


@app.command()
def version():
    print(f"{__app_name__} v{__version__}")
