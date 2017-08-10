FROM debian:jessie

RUN apt-get update -qy
RUN apt-get install -qy uwsgi python-flask

ENV USER tictactoe
ENV PORT 5000

RUN useradd $USER
EXPOSE $PORT

COPY . /app/

USER $USER
CMD ["/usr/bin/python", "/app/app.py", "--host", "0.0.0.0"]


