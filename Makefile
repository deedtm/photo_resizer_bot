ifneq (,$(wildcard ./.env))
    include .env
    export
endif

.PHONY: up down logs build shell

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose up -d --build

logs:
	docker-compose logs -f bot

shell:
	docker-compose exec bot bash

clean:
	docker system prune -a