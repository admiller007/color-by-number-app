# Use Python 3.10 (safer for many ML libraries)
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements and install them (including Detectron2)
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt \
 && pip install 'git+https://github.com/facebookresearch/detectron2.git'

# Copy the rest of the codebase
COPY . .

# Expose the port (adjust if your app uses a different one)
ENV PORT=10000
EXPOSE 10000

# Run your app
CMD ["python", "app.py"]
