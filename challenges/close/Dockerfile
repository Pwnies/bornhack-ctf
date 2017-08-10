FROM debian:jessie

RUN apt-get update -qy
RUN apt-get install -qy python python-dev python-gmpy2

COPY ./server.py .
COPY ./flag      .

RUN chmod +x server.py

EXPOSE 11111

ENTRYPOINT ["./server.py"]
