# OCR API with ocrmypdf

This project provides a **REST API around [ocrmypdf](https://github.com/ocrmypdf/OCRmyPDF)**, allowing you to upload PDFs and receive:

- OCR-extracted text
- PDF with embedded text layer, Base64-encoded

The API is containerized with **Docker** and can be run standalone or together with services like **n8n** or **ERPNext**.

---

## Features

- High-quality OCR using `ocrmypdf`
- Supports English and German (`eng` + `deu`)
- Returns JSON with:
  - `text`: extracted text from PDF
  - `pdf_base64`: Base64-encoded searchable PDF
- Ready for integration with workflow automation tools like n8n
- Dockerized for simple deployment

---

## Project Structure


---

## Installation & Usage

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ocr-api.git
cd ocr-api

### Start container, build if needed
docker-compose up -d --build

```bash
curl -X POST "http://localhost:8000/ocr" -F "file=@example.pdf"

###Response Example:
{
  "text": "Extracted OCR text from PDF...",
  "pdf_base64": "JVBERi0xLjcK..."
}
