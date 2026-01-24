FROM node:20-bullseye-slim AS build


WORKDIR /app

COPY srcs/front/package*.json ./

RUN npm install

COPY srcs/front/. .
COPY docker_prod/front/script.sh .

ENTRYPOINT ["sh", "script.sh"]
