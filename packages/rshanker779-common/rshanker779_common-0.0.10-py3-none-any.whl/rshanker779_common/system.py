import getpass
import platform
import socket


class System:
    HOSTNAME = socket.gethostname()
    USERNAME = getpass.getuser()
    PLATFORM = platform.system()
