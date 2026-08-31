from hedockerssh.services import envmanager


def listinstalledenv():
    envlist = envmanager.listinstalledplatform()
    for i in envlist:
        print(i)

def installplatform(platform: str):
    envmanager.installplatform(platform)

def removeinstalledplatform(platform: str):
    envmanager.removeinstalledplatform(platform)
