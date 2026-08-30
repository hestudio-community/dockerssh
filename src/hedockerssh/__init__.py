import argparse
import platform
import sys

from hedockerssh.controller import container_manager
from hedockerssh.controller import env_manager


import shutil
import subprocess


def dockerchecker() -> bool:
    dockercmd = shutil.which("docker")
    if not dockercmd:
        return False

    r = subprocess.run(
        [dockercmd, "info", "--format", "{{.ServerVersion}}"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    return r.returncode == 0


def main() -> None:
    if not platform.system() == "Linux":
        print("This program runs exclusively on Linux systems.")
        sys.exit(1)
    if not dockerchecker():
        print("You do not have permission to use Docker.")
        sys.exit(1)

    # parser router
    parser = argparse.ArgumentParser()

    # /
    parser_sub = parser.add_subparsers(dest="cmd", required=True, metavar="<command>")
    container_parser = parser_sub.add_parser("container", help="Manager Container.")
    env_parser = parser_sub.add_parser("env", help="Manager Environment.")

    # /env
    env_parser_sub = env_parser.add_subparsers(
        dest="subcmd", required=True, metavar="<command>"
    )
    env_parser_sub.add_parser("list", help="List Installed Environment.")
    install_env_parser = env_parser_sub.add_parser(
        "install", help="Install Environment."
    )
    remove_env_parser = env_parser_sub.add_parser(
        "remove", help="Remove Installed Environment."
    )

    # /env/install
    install_env_parser.add_argument(
        "-p", "--platform", required=True, type=str, help="e.g. linux/amd64"
    )
    install_env_parser.add_argument(
        "-l", "--libc", required=True, type=str, help="e.g. gnu or musl"
    )

    # /env/remove
    remove_env_parser.add_argument(
        "-e",
        "-env",
        "--enviromnemt",
        required=True,
        type=str,
        help="e.g. linux/amd64/gnu",
    )

    # /container
    container_parser_sub = container_parser.add_subparsers(
        dest="subcmd", required=True, metavar="<command>"
    )
    new_container_parser = container_parser_sub.add_parser("new", help="New Container.")
    container_parser_sub.add_parser("list", help="List Container.")
    resetpasswd_container_parser = container_parser_sub.add_parser(
        "resetpasswd", help="Reset Container Password."
    )
    start_container_parser = container_parser_sub.add_parser(
        "start", help="Start Container."
    )
    stop_container_parser = container_parser_sub.add_parser(
        "stop", help="Stop Container."
    )
    restart_container_parser = container_parser_sub.add_parser(
        "restart", help="Restart Container."
    )
    remove_container_parser = container_parser_sub.add_parser(
        "remove", help="Remove Container."
    )

    # /container/new
    new_container_parser.add_argument("-i", "--image", type=str, required=True)
    new_container_parser.add_argument(
        "-e",
        "-env",
        "--enviromnemt",
        type=str,
        required=True,
        help="e.g. linux/amd64/gnu",
    )
    new_container_parser.add_argument("-p", "--port", type=int)
    new_container_parser.add_argument("--passwd", type=str)

    # /container/resetpasswd
    resetpasswd_container_parser.add_argument(
        "container", type=str, metavar="<container>"
    )
    resetpasswd_container_parser.add_argument("--passwd", type=str)

    # /container/start
    start_container_parser.add_argument("container", type=str, metavar="<container>")
    # /container/stop
    stop_container_parser.add_argument("container", type=str, metavar="<container>")
    # /container/restart
    restart_container_parser.add_argument("container", type=str, metavar="<container>")
    # /container/remove
    remove_container_parser.add_argument("container", type=str, metavar="<container>")

    # args router
    args = parser.parse_args()

    match args.cmd:
        case "container":
            match args.subcmd:
                case "new":
                    container_manager.new_container(
                        port=args.port,
                        image=args.image,
                        passwd=args.passwd,
                        env=args.enviromnemt,
                    )
                case "list":
                    container_manager.list_container()
                case "resetpasswd":
                    container_manager.resetpasswd_container(args.passwd, args.container)
                case "start":
                    container_manager.start_container(args.container)
                case "stop":
                    container_manager.stop_container(args.container)
                case "restart":
                    container_manager.restart_container(args.container)
                case "remove":
                    container_manager.remove_container(args.container)
                case _:
                    container_parser.print_usage()
        case "env":
            match args.subcmd:
                case "list":
                    env_manager.listinstalledenv()
                case "install":
                    env_manager.installenv(platform=args.platform, libc=args.libc)
                case "remove":
                    env_manager.removeinstalledenv(env=args.enviromnemt)
                case _:
                    parser.print_usage()
        case _:
            parser.print_usage()
