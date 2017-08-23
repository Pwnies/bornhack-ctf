FROM debian:jessie

RUN apt-get update -qy
RUN apt-get install -qy python-pip python-dev uwsgi
RUN pip install flask

ENV USER tictactoe
ENV PORT 5000

RUN useradd $USER
EXPOSE $PORT

COPY . /app/

USER $USER
ENV FLASK_APP app.py
WORKDIR /app
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--with-threads"]

