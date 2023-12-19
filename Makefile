CONTAINER_NAME :=fastapi-service

.PHONY: build-local
build-local: # Local build/dependency install
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

.PHONY: migration
migration: build # Create new DB migration (DDL/DML)
	docker run -it \
		-v $(PWD)/secrets/:/app/secrets:ro \
		-v $(PWD)/alembic:/app/alembic $(CONTAINER_NAME):latest \
		poetry run alembic -c /app/secrets/alembic.ini revision -m "$(NAME)"

.PHONY: migrate
migrate: # Apply migrations
	docker-compose run --rm $(CONTAINER_NAME) \
		/bin/bash -c "poetry run alembic -c /app/secrets/alembic.ini upgrade head"

.PHONY: rollback-one
rollback-one: # Roll back the recently executed migration
	docker-compose run --rm $(CONTAINER_NAME) \
		/bin/bash -c "poetry run alembic -c /app/secrets/alembic.ini downgrade -1"

.PHONY: migration-history
migration-history: # View migration history
	docker-compse run --rm $(CONTAINER_NAME) \
		/bin/bash -c "poetry run alembic -c /app/secrets/alembic.ini history"

.PHONY: test-unit
test-unit: build-local # Execute unit tests
	poetry run pytest -v --cov-report term-missing --cov=src tests/unit && poetry run coverage report --show-missing

.PHONY: test-coverage
test-coverage: build-local # Generate test coverage report
	poetry run coverage html -d tests/cov

.PHONY: lint
lint: build-local # Execute linting
	poetry run pylint ./src

.PHONY: black-check
black-check: build-local # Check formatting
	black --check --verbose --line-length 120 ./src

.PHONY: black
black: build-local # Reformat application directory
	black --line-length 120 ./src