### CONTAINERS ###

start:
	docker compose -f docker-compose.dev.yaml start

stop:
	docker compose -f docker-compose.dev.yaml stop

build:
	docker compose -f docker-compose.dev.yaml up -d --build

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
