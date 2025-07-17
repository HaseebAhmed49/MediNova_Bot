FROM python:3.13

WORKDIR /app

COPY requirements.txt .

# Install required dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libportaudio2 \
    portaudio19-dev \
    gcc \
    libpq-dev \
    && pip install psycopg2-binary \
    make && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["python", "gradio_app.py"]