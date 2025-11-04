FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y openssh-server openssh-client sudo && \
    mkdir /var/run/sshd

WORKDIR /app


COPY ./jump-server/password.txt .


RUN useradd -m -s /bin/bash jumpuser && \
    usermod -aG sudo jumpuser && \
    echo "jumpuser:$(cat ./password.txt)" | chpasswd 
    
RUN mkdir /home/jumpuser/.ssh && \
    touch /home/jumpuser/.ssh/authorized_keys && \
    chown -R jumpuser:jumpuser /home/jumpuser/.ssh && \
    chmod 700 /home/jumpuser/.ssh && \
    chmod 600 /home/jumpuser/.ssh/authorized_keys

COPY ./jump-server/passwords/jump-server /home/jumpuser/.ssh/jump-server
COPY ./jump-server/passwords/jump-server.pub /home/jumpuser/.ssh/jump-server.pub
COPY ./jump-server/passwords/dev1.pub /home/jumpuser/.ssh/dev1.pub
COPY ./jump-server/passwords/dev2.pub /home/jumpuser/.ssh/dev2.pub

RUN cat /home/jumpuser/.ssh/dev1.pub >> /home/jumpuser/.ssh/authorized_keys && \
    cat /home/jumpuser/.ssh/dev2.pub >> /home/jumpuser/.ssh/authorized_keys && \
    chmod 600 /home/jumpuser/.ssh/jump-server && \
    chmod 644 /home/jumpuser/.ssh/jump-server.pub && \
    chmod 644 /home/jumpuser/.ssh/dev1.pub && \
    chmod 600 /home/jumpuser/.ssh/authorized_keys


RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    echo "AllowAgentForwarding yes" >> /etc/ssh/sshd_config

EXPOSE 22



CMD ["/usr/sbin/sshd", "-D"]


