FROM python:3.10

RUN apt-get update -y \
    && apt-get install -y build-essential

COPY script.sh .

RUN export FLASK_RUN_PORT=8080

CMD ["sh", "script.sh"]