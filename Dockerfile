FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . /app/

# Expose Gradio port
EXPOSE 7860

# Run the application
CMD ["python", "app_v4_final.py"]
