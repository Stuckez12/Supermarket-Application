FROM python:3.13
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

WORKDIR /api

# Install service dependencies
RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync

# Copy in service code
COPY .env .
COPY ./src/backend_services/account ./account
COPY ./src/backend_services/utils ./utils

ENV PATH="/api/.venv/bin:$PATH"
ENV PYTHONPATH="/api:$PYTHONPATH"
