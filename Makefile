###################################################################
# DEVELOPMENT ASSISTANCE
###################################################################

check_imports:
	pycycle --here


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

upgrade_db:
	@docker-compose -f docker-compose.dev.yaml exec account alembic -c /api/account/alembic.ini upgrade head

VERSION ?= -1
downgrade_db:
	@echo "Downgrading to/by $(VERSION) version"
	@docker-compose -f docker-compose.dev.yaml exec account alembic -c /api/account/alembic.ini downgrade $(VERSION)

auto_revision_db:
ifndef MESSAGE
	$(error 'MESSAGE is not set. Usage: make auto_revision_db MESSAGE="message"')
endif
	@docker-compose -f docker-compose.dev.yaml exec account alembic -c /api/account/alembic.ini revision --autogenerate -m "$(MESSAGE)"

seed_db:
	@docker-compose -f docker-compose.dev.yaml exec account python account/app_management.py seed-db


###################################################################
# Testing
###################################################################

unit_tests:
	set PYTHONDONTWRITEBYTECODE=1 && \
	cd src/backend_services && \
	uv run pytest -v tests/unit
