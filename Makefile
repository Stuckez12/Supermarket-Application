###################################################################
# DEVELOPMENT ASSISTANCE
###################################################################

linting:
	uv run black . --check
	uv run mypy .
	uv run flake8 .


################################################################### 
# CONTAINERS
###################################################################

start:
	docker compose -f docker-compose.dev.yaml up -d

stop:
	docker compose -f docker-compose.dev.yaml stop

build:
	docker compose -f docker-compose.dev.yaml build

remove:
	docker compose -f docker-compose.dev.yaml down

logs:
	docker compose -f docker-compose.dev.yaml logs -f

restart:
	$(MAKE) stop
	$(MAKE) start

full-restart:
	$(MAKE) stop
	$(MAKE) build
	$(MAKE) start


###################################################################
# DATABASES
###################################################################

upgrade-db:
	@docker-compose -f docker-compose.dev.yaml exec account alembic -c /api/account/alembic.ini upgrade head

VERSION ?= -1
downgrade-db:
	@echo "Downgrading to/by $(VERSION) version"
	@docker-compose -f docker-compose.dev.yaml exec account alembic -c /api/account/alembic.ini downgrade $(VERSION)

auto-revision-db:
ifndef MESSAGE
	$(error 'MESSAGE is not set. Usage: make auto-revision-db MESSAGE="message"')
endif
	@docker-compose -f docker-compose.dev.yaml exec account alembic -c /api/account/alembic.ini revision --autogenerate -m "$(MESSAGE)"

seed-db:
	@docker-compose -f docker-compose.dev.yaml exec account python account/app_management.py seed-db


###################################################################
# Testing
###################################################################

test-db:
	docker run -d --name postgres-testing -e POSTGRES_PASSWORD=testing -e POSTGRES_USER=testing -e POSTGRES_DB=account -p 5435:5432 postgres:latest

UNIT_TEST ?=
unit-tests:
	set PYTHON_ENV=testing&& \
	set PYTHONDONTWRITEBYTECODE=1 && \
	uv run pytest -v src/backend_services/tests/unit/$(UNIT_TEST) --cov=src

specify-tests:
ifndef TEST
	$(error 'TEST is not set. Usage: make specify-tests TEST="test/route/file.py"')
endif

	set PYTHON_ENV=testing&& \
	set PYTHONDONTWRITEBYTECODE=1 && \
	uv run pytest -vv -s $(TEST)
