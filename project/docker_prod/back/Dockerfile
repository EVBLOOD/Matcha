FROM python:3.10


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y \
    && apt-get install -y build-essential

WORKDIR /app

COPY srcs/back/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY srcs/back/ .

RUN pip install gunicorn

COPY . .

EXPOSE 8080

CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "--bind", "0.0.0.0:8080", "app.app:app"]
# CMD ["flask","--app", "app.app:app", "run",  "--host", "0.0.0.0", "--port", "8080", "--debug"]