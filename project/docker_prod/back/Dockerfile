FROM python:3.10


RUN apt-get update -y \
    && apt-get install -y build-essential

WORKDIR /app

COPY srcs/back/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY srcs/back/ .

CMD ["flask","--app", "app.app:app", "run",  "--host", "0.0.0.0", "--port", "8080", "--debug"]