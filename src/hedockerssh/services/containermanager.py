import subprocess
import json

from hedockerssh.services.core.tools import generatepasswd


def list_container():
    try:
        originoutput = subprocess.run(
            [
                "docker",
                "ps",
                "-a",
                "--filter",
                "label=dockerssh",
                "--format",
                '{"name":"{{.Names}}", "port":{{.Label "dockerssh"}}, "image":"{{.Image}}","libc":"{{.Label "dockerssh-libc"}}", "platform":"{{.Label "dockerssh-platform"}}"}',
            ],
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode())
        return {"code": "ERROR_PROCESS_ERROR"}

    containerliststr = str(originoutput.stdout.decode("utf-8")).split("\n")[:-1]
    containerlist = []
    for i in containerliststr:
        containerlist.append(json.loads(i))
    return {"code": "SUCCESS", "containerlist": containerlist}


def resetpasswd(passwd: str | None, container: str):
    if not container[0:10] == "dockerssh-":
        print("This container is not a dockerssh container.")
        return {"code": "ERROR_NO_DOCKERSSH_CONTAINER"}

    if passwd == None:
        passwd = generatepasswd.generatepasswd()
        print(f"PASSWORD: {passwd}")
        print("The password will only appear ONCE!!!")
    passwd_base64 = generatepasswd.generatepasswdhash(passwd)

    try:
        subprocess.run(
            [
                "docker",
                "exec",
                "-e",
                f"DOCKERSSH_PASSWD={passwd_base64}",
                container,
                "/var/lib/dockerssh/bin/resetpasswd",
            ],
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode())
        return {"code": "ERROR_PROCESS_ERROR"}
    return {"code": "SUCCESS", "passwd": passwd}


def start_container(container: str):
    if not container[0:10] == "dockerssh-":
        print("This container is not a dockerssh container.")
        return {"code": "ERROR_NO_DOCKERSSH_CONTAINER"}
    try:
        subprocess.run(
            [
                "docker",
                "start",
                container,
            ],
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode())
        return {"code": "ERROR_PROCESS_ERROR"}
    return {"code": "SUCCESS"}


def stop_container(container: str):
    if not container[0:10] == "dockerssh-":
        print("This container is not a dockerssh container.")
        return {"code": "ERROR_NO_DOCKERSSH_CONTAINER"}
    try:
        subprocess.run(
            [
                "docker",
                "stop",
                container,
            ],
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode())
        return {"code": "ERROR_PROCESS_ERROR"}
    return {"code": "SUCCESS"}


def restart_container(container: str):
    if not container[0:10] == "dockerssh-":
        print("This container is not a dockerssh container.")
        return {"code": "ERROR_NO_DOCKERSSH_CONTAINER"}
    try:
        subprocess.run(
            [
                "docker",
                "restart",
                container,
            ],
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode())
        return {"code": "ERROR_PROCESS_ERROR"}
    return {"code": "SUCCESS"}


def remove_container(container: str):
    if not container[0:10] == "dockerssh-":
        print("This container is not a dockerssh container.")
        return {"code": "ERROR_NO_DOCKERSSH_CONTAINER"}
    try:
        subprocess.run(
            [
                "docker",
                "stop",
                container,
            ],
            capture_output=True,
            check=True,
        )
        subprocess.run(
            [
                "docker",
                "rm",
                container,
            ],
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode())
        return {"code": "ERROR_PROCESS_ERROR"}
    return {"code": "SUCCESS"}
