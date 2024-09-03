import socket
from time import sleep
from sys import argv

DEFAULT_BROADCAST_PORT = 48372
MSG_MAX_LEN = 1024

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
WHITE='\033[1;37m'
NC='\033[0m'


def main():
    try:
        if len(argv) >= 2:
            host, port = argv[1].split(':') if (len(argv[1].split(':')) == 2) else (argv[1], DEFAULT_BROADCAST_PORT)
        elif len(argv) == 1:
            host, port = "255.255.255.255", DEFAULT_BROADCAST_PORT

        
        host = "255.255.255.255" if (host == "") else host
        port = int(port)

        IPS = ', '.join(set([ip[-1][0] for ip in socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)]))
        print(f'{BLUE}broadcast server{NC} at {WHITE}{socket.gethostname()}{NC}, ips: {WHITE}{IPS}{NC}')
        print(f'{GREEN}start{NC} {WHITE}broadcasting{NC} to {YELLOW}{host}{NC}:{YELLOW}{port}{NC}')

        if len(argv) >= 3:
            msg = bytes(' '.join(argv[2:]), encoding='utf-8')
        else:
            msg = b'Message from ' + bytes(socket.gethostname(), encoding='utf-8')

        
        while True:
            if len(argv) < 2:
                msg = bytes(input(f'Enter message: ({msg[:32].decode(encoding="utf-8")})\n'), encoding='utf-8')
            else:
                sleep(2)
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
                print(f'Sending msg len {YELLOW}{len(msg)}{NC}, {YELLOW}{msg[:32].decode(encoding="utf-8")}{NC}')
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(msg[:MSG_MAX_LEN], (host, port))
            

    except KeyboardInterrupt:
        print(f'\n{RED}stop{NC} {WHITE}listening on{NC} {YELLOW}{host}{NC}:{YELLOW}{port}{NC}')
        exit(0)

if __name__ == '__main__': 
        main()