import getpass
import socket
import platform


class System:
    HOSTNAME = socket.gethostname()
    USERNAME = getpass.getuser()
    PLATFORM = platform.system()
