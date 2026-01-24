FROM python:3.10


RUN apt-get update -y \
    && apt-get install -y build-essential


COPY srcs/back/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY docker/back/script.sh .

RUN export FLASK_RUN_PORT=8080

CMD ["sh", "script.sh"]