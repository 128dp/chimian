FROM python:3.11-slim

WORKDIR /app

# curl is only needed for the container HEALTHCHECK below
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Streamlit needs a writable home/output directory - create one and a
# default output folder that isn't tied to any particular host user.
RUN mkdir -p /data && useradd -m appuser && chown -R appuser:appuser /app /data
USER appuser
ENV HOME=/home/appuser
ENV CHIMIAN_OUTPUT_DIR=/data

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.headless=true"]
