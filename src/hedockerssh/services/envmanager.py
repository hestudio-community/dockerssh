import subprocess
import pathlib
import shutil

from hedockerssh.services.core.env import BASEPATH


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
    base = pathlib.Path("/var/lib/dockerssh/server")
    return sorted("/".join(p.parts[-3:]) for p in base.glob("*/*/*"))


def checkinstalledenv(env: str) -> bool:
    if env in listinstalledenv():
        return True
    else:
        return False


def installenv(platform: str, libc: str):
    if not checkplatformsupport(platform):
        print("Your Docker doesn't support this platform.")
        return {"code": "ERROR_PLATFORM_NOT_SUPPORT"}
    subprocess.run(["bash", f"{BASEPATH}/buildprofile/build.sh", platform, libc])
    return {"code": "SUCCESS"}


def removeinstalledenv(env: str):
    if not checkinstalledenv(env):
        print("The platform is not installed.")
        return {"code": "ERROR_NOT_INSTALLED"}

    try:
        shutil.rmtree(f"/var/lib/dockerssh/server/{env}")
    except PermissionError:
        print("Permission denied.")
        return {"code": "ERROR_NO_PERMISSION"}
    
    return {"code": "SUCCESS"}