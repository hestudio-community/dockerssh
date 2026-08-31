from hedockerssh.services import newcontainer
from hedockerssh.services import containermanager
from rich.table import Table
from rich.console import Console


def new_container(port: int | None, image: str, passwd: str | None, platform: str| None):
    newcontainer.single(port, image, passwd, platform)


def list_container():
    containerlist = containermanager.list_container()["containerlist"]
    table = Table(box=None)
    table.add_column("NAME")
    table.add_column("PORT")
    table.add_column("IMAGE")
    table.add_column("PLATFORM")
    table.add_column("STATUS")

    for i in containerlist:
        table.add_row(i["name"], str(i["port"]), i["image"], i["platform"], i["status"])

    console = Console()
    console.print(table)


def resetpasswd_container(passwd: str | None, container: str):
    containermanager.resetpasswd(passwd, container)


def start_container(container: str):
    containermanager.start_container(container)


def stop_container(container: str):
    containermanager.stop_container(container)


def restart_container(container: str):
    containermanager.restart_container(container)


def remove_container(container: str):
    containermanager.remove_container(container)
