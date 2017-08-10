handout.tar.xz: $(HANDOUT)
	tar -cJf handout.tar.xz $^

docker-build: Dockerfile $(DOCKER_DEPS)
	docker build -t $(DOCKER_NAME) .

docker-start: docker-build
	docker run -d --rm $(DOCKER_ARGS) $(DOCKER_NAME) > .dockerid

docker-stop: .dockerid
	docker kill $(shell cat .dockerid)
	rm .dockerid

handout: handout.tar.xz

.PHONY: docker-stop docker-start docker-build
