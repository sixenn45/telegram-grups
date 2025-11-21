FROM python:3.9-slim

# Set working directory, anjing
WORKDIR /app

# Install system dependencies + cleanup in one layer, bangsat
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for better caching, sialan
COPY requirements.txt .

# Install Python dependencies, dasar bodoh
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files, kontol
COPY . .

# Create sessions directory (CRITICAL buat Telethon), anjing
RUN mkdir -p /app/sessions

# Expose port if needed for web server, bangsat
EXPOSE 8000

# Set proper command, sialan
CMD ["python", "main.py"]
