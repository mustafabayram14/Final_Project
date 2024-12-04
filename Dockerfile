# Use an official lightweight Python image
# Using Python 3.12-slim variant for efficiency
FROM python:3.12-slim-bullseye as base

# Set environment variables for Python and pip configuration
ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=true \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    QR_CODE_DIR=/myapp/qr_codes

# Set the working directory inside the container
WORKDIR /myapp

# Install system dependencies for building Python packages and database support
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file to cache pip installs
COPY ./requirements.txt /myapp/requirements.txt

# Upgrade pip and install Python dependencies from the requirements file
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the rest of the application's code to the container
COPY . .

# Add a script to ensure Minio bucket setup before the application starts
COPY ./setup_minio.py /myapp/setup_minio.py

# Ensure Minio setup script is executable (run as root)
RUN chmod +x /myapp/setup_minio.py

# Add a non-root user and switch to it
RUN useradd -m myuser
USER myuser

# Inform Docker that the container listens on the specified port
EXPOSE 8000

# Set environment variables for Minio (for runtime configuration)
ENV MINIO_ENDPOINT=localhost:9000 \
    MINIO_ACCESS_KEY=your_access_key \
    MINIO_SECRET_KEY=your_secret_key \
    MINIO_BUCKET_NAME=profile-pictures \
    MINIO_SECURE=false

# Run the setup script and then start the application
CMD ["sh", "-c", "python setup_minio.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
