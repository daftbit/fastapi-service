CONTAINER_NAME :=fastapi-service

.PHONY: build-local
build-local:
	poetry install --no-root

.PHONY: build
build: # Build the docker image.
	docker build \
		--target=release \
		-t $(CONTAINER_NAME) .
	docker build \
		--target=test \
		-t $(CONTAINER_NAME):test .


.PHONY: run
run: # Run with docker-compose
	docker-compose stop
	docker-compose up



.PHONY: black-check
black-check: build-local
	black --check --verbose --line-length 120 ./src

.PHONY: black
black: build-local
	black --line-length 120 ./src