FROM debian:jessie

RUN apt-get update -qy
RUN apt-get install -qy python

COPY ./flag      .
COPY ./server.py .

RUN chmod +x server.py

ENTRYPOINT ["./server.py"]
