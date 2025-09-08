from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import tempfile
import os
import subprocess
import base64
import json

app = FastAPI(
    title="OCR API",
    description="REST API around ocrmypdf. Returns OCR text and Base64-encoded PDF.",
    version="1.0.0"
)

@app.post("/ocr")
async def run_ocr(file: UploadFile = File(...)):
    try:
        # Temporäre PDF speichern
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_in:
            tmp_in.write(await file.read())
            tmp_in_path = tmp_in.name
            
        ocrlangs = os.getenv("OCR_LANGS", "deu+eng")
        # Ausgabedateien
        tmp_out = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        tmp_out.close()
        tmp_txt = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        tmp_txt.close()

        # OCRmyPDF ausführen
        subprocess.run(
            ["ocrmypdf", "--sidecar", "--language", ocrlangs, tmp_txt.name, tmp_in_path, tmp_out.name],
            check=True
        )

        # OCR Text einlesen
        with open(tmp_txt.name, "r", encoding="utf-8") as f:
            text = f.read()

        # PDF Base64-codieren
        with open(tmp_out.name, "rb") as f:
            pdf_b64 = base64.b64encode(f.read()).decode("utf-8")

        # Aufräumen
        os.remove(tmp_in_path)
        os.remove(tmp_txt.name)
        os.remove(tmp_out.name)

        # Response
        return JSONResponse(content={
            "text": text,
            "pdf_base64": pdf_b64
        })

    except subprocess.CalledProcessError as e:
        return JSONResponse(content={"error": f"OCRmyPDF failed: {e}"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})
