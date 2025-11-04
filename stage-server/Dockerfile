FROM ubuntu:22.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv openssh-server sudo curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ./stage-server/password.txt .

ARG STAGE_USER=stage-user

RUN useradd -m -s /bin/bash $STAGE_USER && \
    echo "$STAGE_USER:$(cat ./password.txt)" | chpasswd && \
    usermod -aG sudo $STAGE_USER


RUN mkdir -p /home/$STAGE_USER/.ssh && \
    touch /home/$STAGE_USER/.ssh/authorized_keys && \
    chown -R $STAGE_USER:$STAGE_USER /home/$STAGE_USER/.ssh && \
    chmod 700 /home/$STAGE_USER/.ssh && \
    chmod 600 /home/$STAGE_USER/.ssh/authorized_keys

COPY ./stage-server/passwords/stage-server.pub /home/$STAGE_USER/.ssh/
COPY ./stage-server/passwords/stage-server /home/$STAGE_USER/.ssh/




# i copy the password public of dev1 in the authorized-keys of stage server 
# but the jump-server's key not necessary to be in the athorized key of stage server
## the addreess which is in the dir of the command which we want to run in the docker file is run in the container in the run time should be the dir which is exist in the container 
COPY ./stage-server/passwords/dev1.pub /home/$STAGE_USER/.ssh/dev1.pub
COPY ./stage-server/passwords/dev2.pub /home/$STAGE_USER/.ssh/dev2.pub



RUN cat /home/$STAGE_USER/.ssh/dev1.pub >> /home/$STAGE_USER/.ssh/authorized_keys
RUN cat /home/$STAGE_USER/.ssh/dev2.pub >> /home/$STAGE_USER/.ssh/authorized_keys
RUN chown $STAGE_USER:$STAGE_USER /home/$STAGE_USER/.ssh/dev1.pub
RUN chown $STAGE_USER:$STAGE_USER /home/$STAGE_USER/.ssh/dev2.pub

RUN chmod 600 /home/$STAGE_USER/.ssh/dev1.pub
RUN chmod 600 /home/$STAGE_USER/.ssh/dev2.pub


RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config && \
    echo "AllowAgentForwarding yes" >> /etc/ssh/sshd_config

COPY ./stage-server/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./stage-server .

EXPOSE 8000


CMD ["/bin/bash", "-c", "mkdir -p /run/sshd && /usr/sbin/sshd -D & python3 -m uvicorn server:app --host 0.0.0.0 --port 8000"]
    
