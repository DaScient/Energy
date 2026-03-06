FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential   && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md LICENSE /app/
COPY phiak /app/phiak
COPY examples /app/examples
COPY webapp /app/webapp

RUN pip install -U pip && pip install -e ".[vis]"

ENTRYPOINT ["phiak"]
CMD ["--help"]
