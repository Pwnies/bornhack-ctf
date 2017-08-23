FROM debian:jessie

RUN apt-get update -qy
RUN apt-get install -qy socat
RUN apt-get install -qy python

ENV USER utm
ENV PORT 1337

RUN useradd $USER
RUN mkdir /home/$USER
WORKDIR /home/$USER

COPY run-turing.py .
COPY run .
COPY flag .
RUN chmod 555 *

EXPOSE $PORT

ENTRYPOINT ["./run", "./run-turing.py"]

