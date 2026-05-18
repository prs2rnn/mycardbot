FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYTHONPATH=/app/src \
    APP_HOME=/app

WORKDIR $APP_HOME

COPY pyproject.toml poetry.lock README.md LICENSE ./

RUN pip install --no-cache-dir poetry && \
    poetry install --only main --no-root

COPY src/ ./src/

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import mycardbot" || exit 1

CMD ["python", "-m", "mycardbot"]
