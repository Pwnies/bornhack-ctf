FROM debian:jessie

RUN apt-get update -qy
RUN apt-get install -qy python3 python3-dev socat

ENV PORT 1337

WORKDIR /tetris

COPY ./flag .
COPY ./tetrisGame.py .
COPY ./game.py .
COPY ./run .


RUN chmod +x tetrisGame.py
RUN chmod +x game.py
RUN chmod +x run

EXPOSE $PORT

ENTRYPOINT ["./run", "./game.py"]
