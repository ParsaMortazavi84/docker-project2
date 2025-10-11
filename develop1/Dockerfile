FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv openssh-client sudo && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
    
    
WORKDIR /app

COPY ./develop1/passwords/dev1 /root/.ssh/dev1
COPY ./develop1/passwords/dev1.pub /root/.ssh/dev1.pub
RUN chown root:root /root/.ssh/dev1.pub /root/.ssh/dev1.pub

RUN chmod 600 /root/.ssh/dev1 && \
    chmod 644 /root/.ssh/dev1.pub && \
    chown root:root /root/.ssh/dev1 /root/.ssh/dev1.pub


COPY ./develop1/entrypoint.sh ./entrypoint.sh
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

COPY ./develop1/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY /develop1/script.py .
COPY . .


CMD ["python3", "script.py"]