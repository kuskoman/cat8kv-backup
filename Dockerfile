FROM python:3.13-alpine3.20

WORKDIR /app

COPY requirements.txt pyproject.toml ./

RUN apk add --no-cache git bash && \
    pip install --no-cache-dir -r requirements.txt && \
    git config --global user.email "cat8kv-backup@local" && \
    git config --global user.name "cat8kv-backup"

COPY cat8kv/ cat8kv/

RUN pip install --no-cache-dir .

VOLUME ["/app/backups", "/app/git-backups"]

ENTRYPOINT ["cat8kv"]
