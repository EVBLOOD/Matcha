ENV ?= prod

COMPOSE = docker compose -f docker-compose.$(ENV).yml

all:
	$(COMPOSE) up --build -d

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

clean:
	$(COMPOSE) down -v

fclean: clean
	docker system prune --all -f --volumes

ps:
	$(COMPOSE) ps -a

history:
	$(COMPOSE) logs -f