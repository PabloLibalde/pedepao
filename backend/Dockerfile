FROM python:3.13-slim AS base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./alembic.ini
COPY entrypoint.sh ./
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --retries=10 CMD curl -f http://localhost:8000/health || exit 1
CMD ["/app/entrypoint.sh"]
