FROM debian:jessie

RUN apt-get update -qy
RUN apt-get install -qy python3 python3-dev

COPY ./tetrisGame.py .
COPY ./server.py     .

RUN chmod +x tetrisGame.py
RUN chmod +x server.py

EXPOSE 8083

ENTRYPOINT ["./server.py"]
