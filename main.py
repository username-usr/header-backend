from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import GenerateTableRequest, TransformTableRequest, CellMapRequest
from utils import call_ai_cellmap
import uvicorn

app = FastAPI()

# Update CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-cellmap")
async def generate_cellmap(req: CellMapRequest):
    try:
        result = await call_ai_cellmap(req.prompt, req.model)
        return result
    except Exception as e:
        print(f"Error in /generate-cellmap: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process AI request: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)