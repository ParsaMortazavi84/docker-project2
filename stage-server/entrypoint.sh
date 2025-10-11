#!/bin/bash
#!/bin/bash
set -e

mkdir -p /run/sshd &
/usr/sbin/sshd -D

exec python3 -m uvicorn server:app --host 0.0.0.0 --port 8000
