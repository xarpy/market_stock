import os
from pathlib import Path

import click
import pytest
import uvicorn
from IPython import embed

BASE_DIR = Path(__file__).resolve().parent


@click.group()
def cli():
    pass


@click.command("runserver", short_help="Command to execute application")
@click.option(
    "--host", "-h", default="0.0.0.0", help="The host to exposed api access"
)
@click.option(
    "--port", "-p", default=8000, help="The port to exposed api access"
)
@click.option(
    "--reload", "-r", default=True, help="The argument to enable reload mode"
)
def runserver_command(host, port, reload):
    folder_path = os.path.join(BASE_DIR, "logs")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    uvicorn.run("server:app", host=host, port=port, reload=reload)


@click.command("runtest", short_help="Command to execute tests")
@click.option(
    "--list",
    is_flag=True,
    default=False,
    help="Obtain module tests list",
)
@click.option(
    "--node",
    "-n",
    help="Inform the module name and the function you want to run the tests",
)
def test_command(list, node):
    folder_path = os.path.join(BASE_DIR, "tests")
    if not os.path.exists(folder_path):
        print("There is no folder named tests anywhere!")
    if list:
        pytest.main(["--co"])
    if node:
        pytest.main(["-v", f"{folder_path}/{node}"])
    else:
        pytest.main(["-vv", "--cov=."])


@click.command("shell", short_help="Command to execute ipython shell")
def shell_command():
    embed(colors="neutral")


cli.add_command(shell_command)
cli.add_command(runserver_command)
cli.add_command(test_command)

if __name__ == "__main__":
    cli()
