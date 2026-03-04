FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system deps (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends     build-essential   && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md LICENSE /app/
COPY ewis /app/ewis
COPY examples /app/examples

RUN pip install -U pip && pip install -e ".[vis]"

ENTRYPOINT ["ewis"]
CMD ["--help"]
