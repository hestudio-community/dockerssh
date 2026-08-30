import random
import socket


def is_port_in_use(port: int, host: str = "0.0.0.0") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return False
        except OSError:
            return True


def generate_port():
    while True:
        port = random.randint(49152, 65535)
        if not is_port_in_use(port):
            return port
