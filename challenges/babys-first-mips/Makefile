CC=mips-linux-gnu-gcc
CFLAGS=-O3 -static

HANDOUT=firstmips
PORT=1337

firstmips: firstmips.c
	$(CC) $(CFLAGS) firstmips.c -o firstmips

handout.tar.xz: $(HANDOUT)
	tar -cJf handout.tar.xz $^

docker-build: Dockerfile firstmips
	docker build -t firstmips .

docker-start: docker-build
	docker run -d --rm -p $(PORT):1337 firstmips > .dockerid

docker-stop: .dockerid
	docker kill $(shell cat .dockerid)
	rm .dockerid

clean:
	rm -f firstmips .dockerid handout.tar.xz

.PHONY: docker-stop docker-start docker-build clean


    
