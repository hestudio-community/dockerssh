import secrets
import subprocess


from hedockerssh.services.core.env import DATAPATH
from hedockerssh.services.core.tools import port_services
from hedockerssh.services.core.tools import generatepasswd
from hedockerssh.services.envmanager import checkinstalledplatform


def single(port: int | None, image: str, passwd: str | None, platform: str | None) -> dict:
    if platform == None:
        try:
            platformdefault = subprocess.run(
                ["docker", "image", "inspect", "--format", '{{.Os}}/{{.Architecture}}', image],
                capture_output=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(e.stderr.decode())
            return {"code": "ERROR_PROCESS_ERROR"}
        platform = platformdefault.stdout.decode("utf-8").splitlines()[0]

    if not checkinstalledplatform(platform):
        print(f"{platform} is not installed.")
        return {"code": "ERROR_NOT_INSTALLED"}

    if port == None:
        port = port_services.generate_port()
        print(f"PORT: {port}")
    else:
        if not (1 <= port <= 65535):
            print("the port must be between 1 and 65535. exiting...")
            return {"code": "ERROR_PORT_SCOPE"}
        elif port_services.is_port_in_use(port):
            print("this port is already in use. exiting...")
            return {"code": "ERROR_PORT_USED"}

    if passwd == None:
        passwd = generatepasswd.generatepasswd()
        print(f"PASSWORD: {passwd}")
        print("The password will only appear ONCE!!!")
    passwd_base64 = generatepasswd.generatepasswdhash(passwd)

    try:
        subprocess.run(
            [
                "docker",
                "run",
                "--name",
                f"dockerssh-{secrets.token_hex(4)}",
                "--platform",
                platform,
                "-d",
                "-it",
                "-l",
                f"dockerssh={port}",
                "-l",
                f"dockerssh-platform={platform}",
                "-v",
                f"{DATAPATH}/resources/{platform}/out:/var/lib/dockerssh/bin:ro",
                "-p",
                f"{str(port)}:22",
                "-e",
                f"DOCKERSSH_PASSWD={passwd_base64}",
                image,
                "sh",
                "/var/lib/dockerssh/bin/run",
            ],
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode())
        return {"code": "ERROR_PROCESS_ERROR"}

    return {"code": "SUCCESS", "port": port, "passwd": passwd, "image": image}
