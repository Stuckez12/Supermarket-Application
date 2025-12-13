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
COPY ./src/backend_services/gateway ./gateway
COPY ./src/backend_services/utils ./utils

# Copy certificates and service private key
COPY ./src/certificates/certificate ./certificates/certificate
COPY ./src/certificates/private_key/gateway.pem ./certificates/private_key/gateway.pem

ENV PATH="/api/.venv/bin:$PATH"
ENV PYTHONPATH="/api:$PYTHONPATH"
