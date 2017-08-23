FROM debian:stretch

RUN apt-get update
RUN apt-get install -y python2.7 socat

ENV USER cwat
ENV PORT 1337

RUN useradd $USER
RUN mkdir /home/$USER
WORKDIR /home/$USER

COPY cwat.py .
COPY run .
RUN chmod +x run cwat.py

CMD ["/run", "/cwat.py"]