import pathlib
import platform

BASEPATH = pathlib.Path(__file__).resolve().parent.parent.parent

match platform.system():
    case "Linux":
        DATAPATH = "/var/lib/dockerssh"
    case "Darwin":
        DATAPATH = pathlib.Path(pathlib.Path.home(), "Library/Application Support/dockerssh")
