FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml /app/
RUN pip install --no-cache-dir uv pip-tools && \
    pip install --no-cache-dir fastapi uvicorn[standard] pydantic python-dotenv websockets httpx

COPY app /app/app
COPY static /app/static
COPY uvicorn.sh /app/uvicorn.sh
RUN chmod +x /app/uvicorn.sh

EXPOSE 8000
CMD ["/app/uvicorn.sh"]
