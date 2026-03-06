# Multi-stage build for minimal image size using Alpine
# Stage 1: Builder - Install dependencies
FROM python:3.12-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    linux-headers

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Runtime - Minimal production image
FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV APP_HOME=/app

WORKDIR $APP_HOME

# Install only runtime dependencies
RUN apk add --no-cache \
    libpq \
    bash

# Copy wheels from builder and install (single layer to minimize size)
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/* && \
    rm -rf /wheels /root/.cache && \
    pip cache purge 2>/dev/null || true && \
    find /usr/local -type f -name '*.pyc' -delete && \
    find /usr/local -type d -name '__pycache__' -delete && \
    rm -rf /usr/local/lib/python3.12/ensurepip && \
    rm -rf /usr/local/lib/python3.12/idlelib && \
    rm -rf /usr/local/lib/python3.12/tkinter

# Copy project files and set up in a single layer
COPY . .
RUN mkdir -p staticfiles media logs && \
    python manage.py collectstatic --noinput --clear 2>/dev/null || true && \
    adduser -D -u 1000 appuser && \
    chown -R appuser:appuser $APP_HOME

USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000').read()" || exit 1

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "booking_project.wsgi:application"]
