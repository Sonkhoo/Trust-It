from fastapi import FastAPI, File, UploadFile
from ocr_processor import extract_text
from ai_analyzer import analyze_text

app = FastAPI()

@app.post("/detect-spam")
async def detect_spam(image: UploadFile = File(...)):
    # Save temporary file
    with open("temp_image.jpg", "wb") as buffer:
        buffer.write(await image.read())
    
    # OCR Processing
    text = extract_text("temp_image.jpg")
    if not text:
        return {"error": "No text detected"}
    
    # AI Analysis
    analysis = analyze_text(text)
    
    return {
        "text": text,
        "spam_score": round(analysis["spam_score"], 2),
        "explanation": analysis["explanation"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)