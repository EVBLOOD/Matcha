ENV ?= dev

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

certif:
	mkdir docker_prod/nginx/ssl
	mkcert -cert-file docker_prod/nginx/ssl/cert.pem -key-file docker_prod/nginx/ssl/key.pem localhost 127.0.0.1 ::1 your-laptop-ip