FROM python:3.10

RUN apt-get update -y \
    && apt-get install -y build-essential

COPY script.sh .

CMD ["sh", "script.sh"]