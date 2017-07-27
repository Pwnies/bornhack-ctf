FROM debian:jessie

RUN apt-get update -qy
RUN apt-get install -qy socat

ENV USER fmtstr
ENV PORT 1337

ENV FLAG1 "Okay! So you cn leak from the stack"
ENV FLAG2 "GOOD! You can even follow pointers"
ENV FLAG3 "WAUW! You even defeated my ASLR!"

RUN useradd $USER
RUN mkdir /home/$USER
WORKDIR /home/$USER

COPY fmtstr .
COPY run .
RUN chmod 555 *

EXPOSE $PORT

ENTRYPOINT ["./run", "./fmtstr"]

