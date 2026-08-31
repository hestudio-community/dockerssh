import subprocess
import pathlib
import shutil
import platform as pf

from hedockerssh.services.core.env import BASEPATH
from hedockerssh.services.core.env import DATAPATH


def listplatformsupport() -> dict:
    try:
        origin = subprocess.run(
            ["docker", "buildx", "ls", "--format", "{{.Platforms}}"],
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode())
        return {"code": "ERROR_PROCESS_ERROR"}
    return {
        "code": "SUCCESS",
        "platformsupport": origin.stdout.decode("utf-8")
        .replace("\n", "")
        .replace(" ", "")
        .split(","),
    }


def checkplatformsupport(platform: str) -> bool:
    if platform in listplatformsupport()["platformsupport"]:
        return True
    else:
        return False


def listinstalledenv() -> list:
    base = pathlib.Path(f"{DATAPATH}/server")
    return sorted("/".join(p.parts[-3:]) for p in base.glob("*/*/*") if p.is_dir())


def checkinstalledenv(env: str) -> bool:
    if env in listinstalledenv():
        return True
    else:
        return False


def installenv(platform: str, libc: str):
    if not checkplatformsupport(platform):
        print("Your Docker doesn't support this platform.")
        return {"code": "ERROR_PLATFORM_NOT_SUPPORT"}
    subprocess.run(["bash", f"{BASEPATH}/buildprofile/build-{str(pf.system()).lower()}.sh", platform, libc])
    return {"code": "SUCCESS"}


def removeinstalledenv(env: str):
    if not checkinstalledenv(env):
        print("The platform is not installed.")
        return {"code": "ERROR_NOT_INSTALLED"}

    try:
        shutil.rmtree(f"{DATAPATH}/server/{env}")
    except PermissionError:
        print("Permission denied.")
        return {"code": "ERROR_NO_PERMISSION"}
    
    return {"code": "SUCCESS"}