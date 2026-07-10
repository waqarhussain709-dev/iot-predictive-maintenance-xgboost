FROM python:3.10-slim

WORKDIR /app

# Install standard dependencies first to optimize layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files and your model binary
COPY . .

# Expose the standard FastAPI communication port
EXPOSE 8000

# Fire up the live production web server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
