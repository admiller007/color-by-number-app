# Start from a PyTorch image with CUDA support (change to cpu-only if needed)
FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

# Set working directory
WORKDIR /app

# Install system dependencies for OpenCV and Flask
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Detectron2 (matching PyTorch/CUDA version)
RUN pip install git+https://github.com/facebookresearch/detectron2.git

# Copy the rest of the application code
COPY . .

# Set environment variable for Flask port
ENV PORT=10000
EXPOSE 10000

# Run the app
CMD ["python", "app.py"]
