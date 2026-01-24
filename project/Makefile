all_prod : 
	docker compose -f docker-compose.prod.yml up --build -d 

up_prod :
	docker compose -f docker-compose.prod.yml up -d

down_prod:
	docker compose -f docker-compose.prod.yml down

clean_prod:
	docker compose -f docker-compose.prod.yml down -v

fclean_prod: clean_prod
	docker system -f docker-compose.prod.yml prune --all -f --volumes

history_prod:
	docker compose -f docker-compose.prod.yml logs

list_prod: ls_prod
	docker compose -f docker-compose.prod.yml top

ls_prod:
	docker compose -f docker-compose.prod.yml ps -a



all_dev : 
	docker compose -f docker-compose.dev.yml up --build -d 

up_dev :
	docker compose -f docker-compose.dev.yml up -d

down_dev:
	docker compose -f docker-compose.dev.yml down

clean_dev:
	docker compose -f docker-compose.dev.yml down -v

fclean_dev: clean_dev
	docker system -f docker-compose.dev.yml prune --all -f --volumes

history_dev:
	docker compose -f docker-compose.dev.yml logs

list_dev: ls_dev
	docker compose -f docker-compose.dev.yml top

ls_dev:
	docker compose -f docker-compose.dev.yml ps -a