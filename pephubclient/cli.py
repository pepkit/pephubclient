import typer
from requests.exceptions import ConnectionError

from pephubclient import __app_name__, __version__
from pephubclient.exceptions import PEPExistsError, ResponseError
from pephubclient.helpers import MessageHandler
from pephubclient.pephubclient import PEPHubClient

pep_hub_client = PEPHubClient()

app = typer.Typer()


@app.command()
def login():
    """
    Login to PEPhub
    """
    try:
        pep_hub_client.login()
    except ConnectionError:
        MessageHandler.print_error("Failed to log in. Connection Error. Try later.")


@app.command()
def logout():
    """
    Logout
    """
    pep_hub_client.logout()


@app.command()
def pull(
    project_registry_path: str,
    # project_format: str = typer.Option("default", help="Project format in which project should be saved"
    #                                                    "Options: [default, basic, csv, yaml, zip]."),
    force: bool = typer.Option(False, help="Last name of person to greet."),
):
    """
    Download and save project locally.
    """
    try:
        pep_hub_client.pull(project_registry_path, force)

    except ConnectionError:
        MessageHandler.print_error(
            "Failed to download project. Connection Error. Try later."
        )
    except PEPExistsError as err:
        MessageHandler.print_warning(
            f"PEP '{project_registry_path}' already exists. {err}"
        )
    except ResponseError as err:
        MessageHandler.print_error(f"{err}")


@app.command()
def push(
    cfg: str = typer.Argument(
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
    is_private: bool = typer.Option(False, help="Upload project as private."),
):
    """
    Upload/update project in PEPhub
    """
    try:
        pep_hub_client.push(
            cfg=cfg,
            namespace=namespace,
            name=name,
            tag=tag,
            is_private=is_private,
            force=force,
        )
    except ConnectionError:
        MessageHandler.print_error(
            "Failed to upload project. Connection Error. Try later."
        )
    except ResponseError as err:
        MessageHandler.print_error(f"{err}")


@app.command()
def version():
    """
    Package version
    """
    print(f"{__app_name__} v{__version__}")
