CC=gcc
CFLAGS=-O3 -pie -fPIC

HANDOUT=fmtstr.c Makefile
PORT=1337

fmtstr: fmtstr.c
	$(CC) $(CFLAGS) $< -o $%

handout.tar.xz: $(HANDOUT)
	tar -cJf handout.tar.xz $^

docker-build: Dockerfile fmtstr
	docker build -t fmtstr .

docker-start: docker-build
	docker run -d --rm -p $(PORT):1337 fmtstr > .dockerid

docker-stop: .dockerid
	docker kill $(shell cat .dockerid)
	rm .dockerid

.PHONY: docker-stop docker-start docker-build


    
