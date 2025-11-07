"""
REST API for Website Analyzer
Production-ready FastAPI application for website analysis
"""

import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Dict, Any, Union
import uuid
from datetime import datetime
from config import Config
from src.workflows.unified_workflow import analyze

# Set API keys
os.environ["OPENAI_API_KEY"] = Config.get_openai_key()
if Config.PAGESPEED_API_KEY:
    os.environ["PAGESPEED_API_KEY"] = Config.PAGESPEED_API_KEY

# Initialize FastAPI app
app = FastAPI(
    title="Website Analyzer API",
    description="Comprehensive AI-powered website analysis for SEO, Performance, and UI/UX",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for all origins (configure as needed for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for analysis results (use database in production)
analysis_store: Dict[str, Dict[str, Any]] = {}


# Request/Response Models
class AnalysisRequest(BaseModel):
    """Request model for website analysis"""
    input: Union[str, Dict[str, Any]] = Field(
        ...,
        description="URL, HTML code, screenshot path(s), or natural language prompt",
        examples=[
            "https://example.com",
            "Analyze the website: https://nightwatch.io",
            "<html><head><title>Test</title></head><body>...</body></html>",
            {"screenshot": "path/to/screenshot.png"}
        ]
    )
    stream: Optional[bool] = Field(
        default=False,
        description="Whether to stream results (not supported in REST API)"
    )

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "input": "https://nightwatch.io",
                    "stream": False
                },
                {
                    "input": "Analyze the website: https://example.com",
                    "stream": False
                },
                {
                    "input": "<html><head><title>Test</title></head><body><h1>Hello</h1></body></html>",
                    "stream": False
                }
            ]
        }


class AnalysisResponse(BaseModel):
    """Response model for immediate analysis"""
    analysis_id: str = Field(..., description="Unique identifier for this analysis")
    status: str = Field(..., description="Status of the analysis (completed, error)")
    result: Optional[str] = Field(None, description="Analysis results (if completed)")
    error: Optional[str] = Field(None, description="Error message (if error occurred)")
    timestamp: str = Field(..., description="Timestamp of analysis completion")


class AsyncAnalysisResponse(BaseModel):
    """Response model for async analysis"""
    analysis_id: str = Field(..., description="Unique identifier for this analysis")
    status: str = Field(..., description="Status of the analysis (pending, processing, completed, error)")
    message: str = Field(..., description="Status message")


class AnalysisStatusResponse(BaseModel):
    """Response model for checking analysis status"""
    analysis_id: str = Field(..., description="Unique identifier for this analysis")
    status: str = Field(..., description="Status of the analysis")
    result: Optional[str] = Field(None, description="Analysis results (if completed)")
    error: Optional[str] = Field(None, description="Error message (if error occurred)")
    timestamp: str = Field(..., description="Timestamp of last update")


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str = Field(..., description="API health status")
    version: str = Field(..., description="API version")
    openai_configured: bool = Field(..., description="Whether OpenAI API key is configured")
    pagespeed_configured: bool = Field(..., description="Whether PageSpeed API key is configured")


# Background task for async analysis
def run_analysis_task(analysis_id: str, user_input: Union[str, Dict[str, Any]]):
    """Background task to run website analysis"""
    try:
        # Update status to processing
        analysis_store[analysis_id]["status"] = "processing"
        analysis_store[analysis_id]["timestamp"] = datetime.now().isoformat()

        # Run analysis
        result = analyze(user_input, stream=False)

        # Store results
        analysis_store[analysis_id]["status"] = "completed"
        analysis_store[analysis_id]["result"] = result
        analysis_store[analysis_id]["timestamp"] = datetime.now().isoformat()

    except Exception as e:
        # Store error
        analysis_store[analysis_id]["status"] = "error"
        analysis_store[analysis_id]["error"] = str(e)
        analysis_store[analysis_id]["timestamp"] = datetime.now().isoformat()


# API Endpoints
@app.get("/", tags=["General"])
async def root():
    """Root endpoint - API information"""
    return {
        "name": "Website Analyzer API",
        "version": "1.0.0",
        "description": "Comprehensive AI-powered website analysis",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "analyze": "/analyze",
            "analyze_async": "/analyze/async",
            "status": "/analyze/{analysis_id}"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        openai_configured=bool(Config.OPENAI_API_KEY),
        pagespeed_configured=bool(Config.PAGESPEED_API_KEY)
    )


@app.post("/analyze", response_model=AnalysisResponse, tags=["Analysis"])
async def analyze_website(request: AnalysisRequest):
    """
    Analyze a website synchronously (blocks until complete)

    **Input Types:**
    - URL: `https://example.com`
    - Natural language: `"Analyze the website: https://example.com"`
    - HTML: `<html>...</html>`
    - Screenshot: `{"screenshot": "path.png"}` or `{"screenshots": {...}}`

    **Analysis Includes:**
    - SEO optimization and content quality
    - Performance metrics (Core Web Vitals)
    - UI/UX design (with vision AI)
    - Executive summary with recommendations
    """
    analysis_id = str(uuid.uuid4())

    try:
        # Validate configuration
        if not Config.validate_required_keys():
            raise HTTPException(
                status_code=500,
                detail="API keys not configured. Please set OPENAI_API_KEY in config.py"
            )

        # Run analysis
        result = analyze(request.input, stream=False)

        # Store results
        analysis_store[analysis_id] = {
            "status": "completed",
            "result": result,
            "error": None,
            "timestamp": datetime.now().isoformat()
        }

        return AnalysisResponse(
            analysis_id=analysis_id,
            status="completed",
            result=result,
            error=None,
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        # Store error
        analysis_store[analysis_id] = {
            "status": "error",
            "result": None,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/async", response_model=AsyncAnalysisResponse, tags=["Analysis"])
async def analyze_website_async(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """
    Analyze a website asynchronously (returns immediately with analysis_id)

    Use the `/analyze/{analysis_id}` endpoint to check status and retrieve results.

    **Input Types:**
    - URL: `https://example.com`
    - Natural language: `"Analyze the website: https://example.com"`
    - HTML: `<html>...</html>`
    - Screenshot: `{"screenshot": "path.png"}` or `{"screenshots": {...}}`
    """
    # Validate configuration
    if not Config.validate_required_keys():
        raise HTTPException(
            status_code=500,
            detail="API keys not configured. Please set OPENAI_API_KEY in config.py"
        )

    # Generate analysis ID
    analysis_id = str(uuid.uuid4())

    # Initialize analysis record
    analysis_store[analysis_id] = {
        "status": "pending",
        "result": None,
        "error": None,
        "timestamp": datetime.now().isoformat()
    }

    # Add background task
    background_tasks.add_task(run_analysis_task, analysis_id, request.input)

    return AsyncAnalysisResponse(
        analysis_id=analysis_id,
        status="pending",
        message=f"Analysis started. Use GET /analyze/{analysis_id} to check status."
    )


@app.get("/analyze/{analysis_id}", response_model=AnalysisStatusResponse, tags=["Analysis"])
async def get_analysis_status(analysis_id: str):
    """
    Get the status and results of an analysis

    **Status Values:**
    - `pending`: Analysis queued but not started
    - `processing`: Analysis in progress
    - `completed`: Analysis finished successfully
    - `error`: Analysis failed
    """
    if analysis_id not in analysis_store:
        raise HTTPException(status_code=404, detail="Analysis ID not found")

    analysis = analysis_store[analysis_id]

    return AnalysisStatusResponse(
        analysis_id=analysis_id,
        status=analysis["status"],
        result=analysis.get("result"),
        error=analysis.get("error"),
        timestamp=analysis["timestamp"]
    )


@app.delete("/analyze/{analysis_id}", tags=["Analysis"])
async def delete_analysis(analysis_id: str):
    """Delete an analysis record"""
    if analysis_id not in analysis_store:
        raise HTTPException(status_code=404, detail="Analysis ID not found")

    del analysis_store[analysis_id]

    return {"message": f"Analysis {analysis_id} deleted successfully"}


# Run with: uvicorn api:app --host 0.0.0.0 --port 8000 --reload
if __name__ == "__main__":
    import uvicorn

    # Validate configuration
    print("\n" + "="*70)
    print("WEBSITE ANALYZER REST API")
    print("="*70)

    Config.print_status()

    if not Config.validate_required_keys():
        print("\n[!] Please configure required API keys in config.py")
        exit(1)

    print("\nAPI Features:")
    print("  - Synchronous analysis (/analyze)")
    print("  - Asynchronous analysis (/analyze/async)")
    print("  - Status checking (/analyze/{id})")
    print("  - Health monitoring (/health)")
    print("  - OpenAPI documentation (/docs)")

    print("\nStarting API server...")
    print("  API: http://localhost:8000")
    print("  Docs: http://localhost:8000/docs")
    print("  ReDoc: http://localhost:8000/redoc")
    print("="*70 + "\n")

    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
