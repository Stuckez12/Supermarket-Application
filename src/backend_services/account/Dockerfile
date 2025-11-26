FROM python:3.13

WORKDIR /api

# Install service dependencies
RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync

# Copy in service code
COPY ./src/backend_services/account ./account
COPY ./src/backend_services/utils ./utils

ENV PATH="/api/.venv/bin:$PATH"
ENV PYTHONPATH="/api:$PYTHONPATH"
