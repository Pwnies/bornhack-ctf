FROM debian

RUN apt-get update -qy
RUN apt-get install -qy python python-pip
RUN pip install unicorn

COPY ./flag      .
COPY ./server.py .

RUN chmod +x server.py

ENTRYPOINT ["./server.py"]
