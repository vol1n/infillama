from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional
import os

app = FastAPI()

# Serve static files from the "public" directory
app.mount("/static", StaticFiles(directory="public"), name="static")

# Redirect root to the dashboard.html
@app.get("/")
async def read_root():
    return FileResponse('public/dashboard.html')

# Example endpoints
@app.get("/generate-examples")
async def generate_examples(instructions: Optional[str] = None):
    try:
        # Replace this with your actual function to generate examples
        examples = "Imaginary function result"
        return {"examples": examples}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/submit-selection")
async def submit_selection(selected_example: str):
    try:
        # Replace with your actual function to process selected examples
        result = "Selected example processed"
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/submit-feedback")
async def submit_feedback(feedback: str):
    try:
        # Replace with your actual function to handle feedback
        result = "Feedback received"
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
