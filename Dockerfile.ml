# Dockerfile.ml (Machine Learning Environment)
FROM tensorflow/tensorflow:2.13.0-gpu

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        git \
        wget \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python ML dependencies
COPY requirements.ml.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.ml.txt

# Copy project
COPY . /app/

# Create directories
RUN mkdir -p /app/ml_models /app/datasets

# Create non-root user
RUN adduser --disabled-password --gecos '' mluser \
    && chown -R mluser:mluser /app
USER mluser

# Default command (keep container running)
CMD ["tail", "-f", "/dev/null"]