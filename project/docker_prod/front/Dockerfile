FROM node:20-bullseye-slim AS build


WORKDIR /app

COPY srcs/front/package*.json ./

RUN npm install

COPY srcs/front/. .

ARG VITE_BACKEND_LINK
ARG VITE_SOCKET_LINK

ENV VITE_SOCKET_LINK=$VITE_SOCKET_LINK
ENV VITE_BACKEND_LINK=$VITE_BACKEND_LINK

RUN npm run build

FROM nginx:stable-alpine AS production

COPY --from=build /app/dist /usr/share/nginx/html

COPY docker_prod/front/nginx.conf /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]
