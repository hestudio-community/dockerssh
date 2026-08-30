from rich.table import Table
from rich.console import Console

from hedockerssh.services import envmanager


def listinstalledenv():
    envlist = envmanager.listinstalledenv()
    table = Table()
    table.add_column("PLATFORM")
    table.add_column("LIBC")

    for i in envlist:
        base, libc = i.rsplit("/", 1)
        table.add_row(base, libc)

    console = Console()
    console.print(table)


def installenv(platform: str, libc: str):
    envmanager.installenv(platform, libc)

def removeinstalledenv(env: str):
    envmanager.removeinstalledenv(env)
