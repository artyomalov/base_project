# Stage 1: Build Environment
FROM python:3.12-alpine3.19 AS base

WORKDIR /app

# Copy requirements and install dependencies
COPY ./requirements.txt .

RUN python -m venv .venv && \
    echo "export PATH=\"/app/.venv/bin:\$PATH\"" >> /etc/profile.d/venv.sh && \
    /app/.venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .


# Stage 2: Runtime Environment
FROM python:3.12-alpine3.19

WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"

COPY --from=base /app .

COPY ./entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 8000


ENTRYPOINT ["./entrypoint.sh"]