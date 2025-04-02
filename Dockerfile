# Use Python 3.10 (safer for many ML libraries)
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt \
 && pip install 'git+https://github.com/facebookresearch/detectron2.git'

# Copy rest of the app
COPY . .

# Set environment port
ENV PORT=10000
EXPOSE 10000

# Run the app
CMD ["python", "app.py"]
