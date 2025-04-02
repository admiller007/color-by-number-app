# Use a slim base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system-level dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir 'git+https://github.com/facebookresearch/detectron2.git'

# Copy your app code
COPY . .

# Set environment variables
ENV PORT=10000 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Expose port for external access
EXPOSE 10000

# Run the app (adjust based on framework)
CMD ["python", "app.py"]
