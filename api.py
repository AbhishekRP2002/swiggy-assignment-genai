"""
source code for fastapi interface for the Personal Assistant agent
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional  # noqa
import uvicorn
from src.agent import PersonalAssistant

app = FastAPI(
    title="Personal Assistant API",
    description="API for processing user queries with the personal assistant",
)

assistant = PersonalAssistant()


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    result: Dict[str, Any]


@app.post("/process-query", response_model=QueryResponse)
async def process_query(request: QueryRequest) -> Dict[str, Any]:
    """
    Process a user query and return structured information
    """
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        result = assistant.process_query(request.query)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
