all : 
	docker compose up --build -d 

up :
	docker compose up -d

down:
	docker compose down

clean:
	docker compose down -v

fclean: clean
	docker system prune --all -f --volumes

history:
	docker compose logs

list: ls
	docker compose top

ls:
	docker compose ps -a