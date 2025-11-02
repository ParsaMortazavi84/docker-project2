import paramiko
import socket
import select
import threading
import time

JUMP_HOST = "jump-server"
JUMP_USER = "jumpuser"
STAGE_HOST = "stage-server"
STAGE_PORT = 8000
LOCAL_PORT = 8000

WAIT_TIME = 5


def handler(chan, sock):
    while True:
        r, _, _ = select.select([sock, chan], [], [])
        if sock in r:
            data = sock.recv(1024)
            if not data:
                break
            chan.send(data)
        if chan in r:
            data = chan.recv(1024)
            if not data:
                break
            sock.send(data)
    chan.close()
    sock.close()


def forward_tunnel(local_port, remote_host, remote_port, transport):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", local_port))
    sock.listen(100)
    print(f"[+] Forwarding localhost:{local_port} → {remote_host}:{remote_port}")

    while True:
        client, addr = sock.accept()
        print(f"[+] Connection from {addr}")
        chan = transport.open_channel(
            "direct-tcpip",
            (remote_host, remote_port),
            addr
        )
        threading.Thread(target=handler, args=(chan, client), daemon=True).start()


while True:
    try:
        print("[+] Connecting to jump server...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(JUMP_HOST, username=JUMP_USER, port=22, key_filename="/root/.ssh/dev2", look_for_keys=False,
                       allow_agent=False)
        print("[+] Connected to jump server.")

        transport = client.get_transport()
        forward_tunnel(LOCAL_PORT, STAGE_HOST, STAGE_PORT, transport)
    except Exception as e:
        print(f"[!] Error: {e}")
        time.sleep(WAIT_TIME)
