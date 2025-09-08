# -----------------------------
# OCR API Dockerfile
# -----------------------------

# Basis-Image: schlankes Debian mit Python 3.12
FROM python:3.12-slim

# Systempakete installieren
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-deu \
    tesseract-ocr-eng \
    poppler-utils \
    ghostscript \
    qpdf \
    build-essential \
    libffi-dev \
    pkg-config \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis
WORKDIR /app

# Python-Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Anwendungscode kopieren
COPY . .

# Port freigeben
EXPOSE 8000

# Start der API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
