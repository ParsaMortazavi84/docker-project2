import paramiko
from paramiko.agent import AgentRequestHandler
import time
WAIT_TIME = 5
while 1:
    try:
        jump = paramiko.SSHClient()
        jump.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        jump.connect("jump-server", username='jumpuser', port=22)

        jump_transport = jump.get_transport()
        dest_addr = ("stage-server", 22)
        local_addr = ("127.0.0.1", 22)
        channel = jump_transport.open_channel("direct-tcpip", dest_addr, local_addr)

        target_transport = paramiko.Transport(channel)
        target_transport.start_client()

        AgentRequestHandler(target_transport.open_session())

        agent = paramiko.Agent()
        keys = agent.get_keys()
        if len(keys) == 0:
            raise Exception("No keys found")
        key = keys[0]

        target_transport.auth_publickey("stage-user", key)

        session = target_transport.open_session()
        session.exec_command("whoami; hostname")
        print(session.recv(4096).decode())
    except Exception as e:
        time.sleep(WAIT_TIME)

session.close()
target_transport.close()
jump.close()
