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

downgrade_db:
ifndef VERSION
	VERSION=-1
	@echo "VERSION not defined. Defaulting to downgrade to previous version"
endif
	@docker-compose -f docker-compose.dev.yaml exec account alembic -c /api/account/alembic.ini downgrade $(VERSION)

auto_revision_db:
ifndef MESSAGE
	$(error 'MESSAGE is not set. Usage: make auto_revision_db MESSAGE="message"')
endif
	@echo "Running with PARAM=$(PARAM)"
	@docker-compose -f docker-compose.dev.yaml exec account alembic -c /api/account/alembic.ini revision --autogenerate -m "$(PARAM)"
