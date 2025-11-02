FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv openssh-client sudo curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./develop2/passwords/dev2 /root/.ssh/dev2
COPY ./develop2/passwords/dev2.pub /root/.ssh/dev2.pub


RUN chmod 600 /root/.ssh/dev2 && \
    chmod 644 /root/.ssh/dev2.pub && \
    chown root:root /root/.ssh/dev2 /root/.ssh/dev2.pub



COPY ./develop2/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY /develop2/script.py .
COPY ./develop2 .


CMD ["python3", "script.py"]
