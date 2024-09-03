import socket
import datetime
from sys import argv

DEFAULT_BROADCAST_PORT = 48372
MSG_MAX_LEN = 1024

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
WHITE='\033[1;37m'
NC='\033[0m'

if len(argv) >= 2:
    host, port = argv[1].split(':') if (len(argv[1].split(':')) == 2) else (argv[1], DEFAULT_BROADCAST_PORT)
elif len(argv) == 1:
    host, port = "", DEFAULT_BROADCAST_PORT


    

host = "0.0.0.0" if host == "" else host

port = int(port)

try:
        # interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
    # allips = [ip[-1][0] for ip in interfaces]
    IPS = ', '.join(set([ip[-1][0] for ip in socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)]))
    print(f'{BLUE}broadcast client{NC} at {WHITE}{socket.gethostname()}{NC}, ips: {WHITE}{IPS}{NC}')
    print(f'{GREEN}start{NC} {WHITE}sending on{NC} {YELLOW}{host}{NC}:{YELLOW}{port}{NC}')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind((host, port))
        while True:
            data, addr = sock.recvfrom(MSG_MAX_LEN)
            sender_host, sender_port = addr
            DATA = data[:32].decode(encoding='utf-8')
            print(f'{GREEN}{sender_host}{NC} {BLUE}->{NC} {YELLOW}{DATA}{NC}')
except KeyboardInterrupt:
    print(f'\n{RED}stop{NC} {WHITE}listening on{NC} {YELLOW}{host}{NC}:{YELLOW}{port}{NC}')
    exit(0)