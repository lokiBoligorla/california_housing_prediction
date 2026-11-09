
# Use Python 3.11
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose application port
EXPOSE 5000

# Start Flask application using Gunicorn
CMD ["sh", "-c", "gunicorn --workers 4 --bind 0.0.0.0:${PORT:-5000} app:app"]
