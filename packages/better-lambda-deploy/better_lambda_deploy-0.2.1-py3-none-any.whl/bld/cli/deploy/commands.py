from ...deployer import Deployer
import click


@click.command()
@click.option("--name", required=True, help="The name of the project to deploy.")
@click.option("--dir", default="./", help="The directory to deploy as a BLD project.")
@click.option(
    "--docker", is_flag=True, default=False, help="Run the SAM build in Docker."
)
@click.option(
    "--local", is_flag=True, default=False, help="Build locally instead of using SAM."
)
def deploy(name, dir, docker, local):
    deployer = Deployer(name, dir, docker=docker, local=local)
    deployer.deploy()
