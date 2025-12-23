## Project Overview

This project demonstrates the deployment of four Docker containers:

- `developer1`
- `developer2`
- `jump-server`
- `stage-server`

The goal of this project is to **access and verify a FastAPI service running on the stage-server through a jump server**,  
without providing direct access to the stage server itself.

Only the FastAPI service is exposed, and interaction is limited to HTTP requests such as:

```bash
curl http://<ip>:<port>/weather

Access Methods
Two different secure approaches are implemented to access the FastAPI service:

🔹 Method 1 – SSH Agent Forwarding (developer1)

In this method, the developer1 container connects to the jump-server using SSH agent forwarding.
The jump server then forwards the FastAPI service port (e.g. 8000) to allow HTTP access to the service running on the stage-server.
No direct SSH access to the stage server is allowed
Only service-level (HTTP) access is permitted via port forwarding

🔹 Method 2 – Passwordless SSH (developer2)

In this approach, key-based (passwordless) SSH authentication is used.
The developer2 container forwards the FastAPI service port on the stage-server through the jump-server, enabling access to the service via HTTP requests.
Technical Implementation

Both access methods are implemented using Python scripts
The Paramiko library is used for SSH connections and port forwarding
The stage server is never accessed directly; only the FastAPI service is exposed


Docker Network Architecture

The Docker Compose configuration uses isolated networks to simulate a production-like environment:
developer1 and jump-server share one Docker network
jump-server and stage-server share a separate internal network
The same network isolation applies to developer2
This architecture reflects a real-world Jump Server (Bastion Host) pattern, where internal services are accessed securely without exposing internal servers.
