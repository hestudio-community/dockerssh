import subprocess
import pathlib
import shutil
import platform as pf
import json

from hedockerssh.services.core.env import BASEPATH
from hedockerssh.services.core.env import DATAPATH


def listplatformsupport() -> dict:
    try:
        origin = subprocess.run(
            ["docker", "buildx", "ls", "--format", "json"],
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode())
        return {"code": "ERROR_PROCESS_ERROR"}

    result = list(map(json.loads, filter(None, origin.stdout.decode("utf-8").splitlines())))
    print(result[0]["Nodes"][0]["Platforms"])
    return {
        "code": "SUCCESS",
        "platformsupport": result[0]["Nodes"][0]["Platforms"]
    }


def checkplatformsupport(platform: str) -> bool:
    if platform in listplatformsupport()["platformsupport"]:
        return True
    else:
        return False


def listinstalledplatform() -> list:
    base = pathlib.Path(f"{DATAPATH}/resources")
    installed = []
    for i in base.glob("*/**/out"):
        installed.append(str(i.parent.relative_to(base)))
    return sorted(installed)


def checkinstalledplatform(platform: str) -> bool:
    if platform in listinstalledplatform():
        return True
    else:
        return False


def installplatform(platform: str):
    if not checkplatformsupport(platform):
        print("Your Docker doesn't support this platform.")
        return {"code": "ERROR_PLATFORM_NOT_SUPPORT"}
    subprocess.run(["bash", f"{BASEPATH}/buildprofile/build-{str(pf.system()).lower()}.sh", platform])
    return {"code": "SUCCESS"}


def removeinstalledplatform(platform: str):
    if not checkinstalledplatform(platform):
        print("The platform is not installed.")
        return {"code": "ERROR_NOT_INSTALLED"}

    try:
        shutil.rmtree(f"{DATAPATH}/resources/{platform}")
    except PermissionError:
        print("Permission denied.")
        return {"code": "ERROR_NO_PERMISSION"}
    
    return {"code": "SUCCESS"}