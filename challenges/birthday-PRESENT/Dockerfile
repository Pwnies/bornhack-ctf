FROM debian:jessie

RUN apt-get update -qy
RUN apt-get install -qy socat

COPY ./birthday .
COPY ./run      .
COPY ./flag.fmt .

ENV PORT 1337

RUN chmod +x run
RUN chmod +x birthday

EXPOSE $PORT

ENTRYPOINT ["./run", "./birthday"]
