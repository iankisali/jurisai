from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import asyncio
import uuid
from datetime import datetime
import json
import os
from pathlib import Path

from .crew import JurisAIOrchestrator

# Initialize FastAPI app
app = FastAPI(
    title="JurisAI API",
    description="AI-powered legal assistance platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store task results (in production, use a proper database)
task_store: Dict[str, Dict[str, Any]] = {}

# Initialize the orchestrator once at startup
orchestrator = None

@app.on_event("startup")
async def startup_event():
    """Initialize the JurisAI Orchestrator on startup"""
    global orchestrator
    try:
        orchestrator = JurisAIOrchestrator()
        print("✅ JurisAI Orchestrator initialized on startup")
    except Exception as e:
        print(f"❌ Failed to initialize orchestrator: {e}")

# Pydantic models for request/response
class LegalQueryRequest(BaseModel):
    query: str
    case_type: Optional[str] = "general"
    jurisdiction: Optional[str] = "federal"
    urgency: Optional[str] = "normal"
    additional_context: Optional[str] = None

class DocumentAnalysisRequest(BaseModel):
    document_text: str
    analysis_type: Optional[str] = "comprehensive"
    specific_sections: Optional[List[str]] = None

class ClientIntakeRequest(BaseModel):
    client_name: str
    case_description: str
    case_type: str
    jurisdiction: Optional[str] = "federal"
    preferred_outcome: Optional[str] = None
    budget_range: Optional[str] = None
    timeline: Optional[str] = None

class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: str
    completed_at: Optional[str] = None

# Map client types based on case types
def get_client_type(case_type: str) -> str:
    """Determine client type based on case type"""
    business_cases = ['corporate', 'intellectual_property', 'business']
    lawyer_cases = ['complex_litigation', 'appeals']
    
    if case_type in business_cases:
        return 'business'
    elif case_type in lawyer_cases:
        return 'lawyer'
    else:
        return 'citizen'

# Background task executor for legal queries
async def process_legal_query_task(task_id: str, inputs: dict):
    """Execute legal query processing in background"""
    try:
        task_store[task_id]["status"] = "processing"
        
        # Extract parameters
        query = inputs['query']
        client_type = get_client_type(inputs.get('case_type', 'general'))
        jurisdiction = inputs.get('jurisdiction', 'federal')
        
        # Add additional context to query if provided
        if inputs.get('additional_context'):
            query = f"{query}\n\nAdditional Context: {inputs['additional_context']}"
        
        # Process through orchestrator
        result = orchestrator.process_legal_query(
            query=query,
            client_type=client_type,
            jurisdiction=jurisdiction
        )
        
        # Store results
        if result['status'] == 'success':
            task_store[task_id]["status"] = "completed"
            task_store[task_id]["result"] = {
                "output": str(result['result']),
                "client_type": result['client_type'],
                "query": result['query'],
                "task_type": "legal_query"
            }
        else:
            task_store[task_id]["status"] = "failed"
            task_store[task_id]["error"] = result.get('error', 'Unknown error occurred')
        
        task_store[task_id]["completed_at"] = datetime.now().isoformat()
        
    except Exception as e:
        task_store[task_id]["status"] = "failed"
        task_store[task_id]["error"] = str(e)
        task_store[task_id]["completed_at"] = datetime.now().isoformat()

# Background task executor for document analysis
async def process_document_analysis_task(task_id: str, inputs: dict):
    """Execute document analysis in background"""
    try:
        task_store[task_id]["status"] = "processing"
        
        # Extract parameters
        document_text = inputs['document_text']
        analysis_type = inputs.get('analysis_type', 'general')
        
        # Map analysis types to focus areas
        analysis_focus_map = {
            'comprehensive': 'general',
            'risk_assessment': 'risk',
            'contract_review': 'contract',
            'compliance': 'compliance'
        }
        analysis_focus = analysis_focus_map.get(analysis_type, 'general')
        
        # Determine client type (default to citizen for document analysis)
        client_type = inputs.get('client_type', 'citizen')
        
        # Process through orchestrator
        result = orchestrator.analyze_document(
            document_content=document_text,
            analysis_focus=analysis_focus,
            client_type=client_type
        )
        
        # Store results
        if result['status'] == 'success':
            task_store[task_id]["status"] = "completed"
            task_store[task_id]["result"] = {
                "output": str(result['result']),
                "analysis_focus": result['analysis_focus'],
                "client_type": result['client_type'],
                "task_type": "document_analysis"
            }
        else:
            task_store[task_id]["status"] = "failed"
            task_store[task_id]["error"] = result.get('error', 'Unknown error occurred')
        
        task_store[task_id]["completed_at"] = datetime.now().isoformat()
        
    except Exception as e:
        task_store[task_id]["status"] = "failed"
        task_store[task_id]["error"] = str(e)
        task_store[task_id]["completed_at"] = datetime.now().isoformat()

# Background task executor for client intake
async def process_client_intake_task(task_id: str, inputs: dict):
    """Execute client intake processing in background"""
    try:
        task_store[task_id]["status"] = "processing"
        
        # Construct a comprehensive query from client intake information
        query = f"""
        Client Name: {inputs['client_name']}
        Case Type: {inputs['case_type']}
        
        Case Description:
        {inputs['case_description']}
        
        Jurisdiction: {inputs.get('jurisdiction', 'Not specified')}
        Preferred Outcome: {inputs.get('preferred_outcome', 'Not specified')}
        Budget Range: {inputs.get('budget_range', 'Not specified')}
        Timeline: {inputs.get('timeline', 'Not specified')}
        
        Please provide comprehensive legal advice and next steps for this client.
        """
        
        # Determine client type based on case type
        client_type = get_client_type(inputs['case_type'])
        jurisdiction = inputs.get('jurisdiction', 'federal')
        
        # Process through orchestrator as a legal query
        result = orchestrator.process_legal_query(
            query=query,
            client_type=client_type,
            jurisdiction=jurisdiction
        )
        
        # Store results
        if result['status'] == 'success':
            task_store[task_id]["status"] = "completed"
            task_store[task_id]["result"] = {
                "output": str(result['result']),
                "client_name": inputs['client_name'],
                "case_type": inputs['case_type'],
                "task_type": "client_intake"
            }
        else:
            task_store[task_id]["status"] = "failed"
            task_store[task_id]["error"] = result.get('error', 'Unknown error occurred')
        
        task_store[task_id]["completed_at"] = datetime.now().isoformat()
        
    except Exception as e:
        task_store[task_id]["status"] = "failed"
        task_store[task_id]["error"] = str(e)
        task_store[task_id]["completed_at"] = datetime.now().isoformat()

# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "JurisAI API is running",
        "version": "1.0.0",
        "orchestrator_status": "initialized" if orchestrator else "not initialized",
        "endpoints": [
            "/api/legal-query",
            "/api/analyze-document", 
            "/api/client-intake",
            "/api/task-status/{task_id}",
            "/api/tasks",
            "/health"
        ]
    }

@app.post("/api/legal-query", response_model=TaskResponse)
async def legal_query(request: LegalQueryRequest, background_tasks: BackgroundTasks):
    """Submit a legal query for AI processing"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Service not ready. Orchestrator not initialized.")
    
    task_id = str(uuid.uuid4())
    
    # Initialize task in store
    task_store[task_id] = {
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "type": "legal_query"
    }
    
    # Prepare inputs
    inputs = {
        "query": request.query,
        "case_type": request.case_type,
        "jurisdiction": request.jurisdiction or "federal",
        "additional_context": request.additional_context
    }
    
    # Add background task
    background_tasks.add_task(process_legal_query_task, task_id, inputs)
    
    return TaskResponse(
        task_id=task_id,
        status="pending",
        message="Legal query submitted for processing"
    )

@app.post("/api/analyze-document", response_model=TaskResponse)
async def analyze_document(request: DocumentAnalysisRequest, background_tasks: BackgroundTasks):
    """Submit a document for legal analysis"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Service not ready. Orchestrator not initialized.")
    
    task_id = str(uuid.uuid4())
    
    task_store[task_id] = {
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "type": "document_analysis"
    }
    
    inputs = {
        "document_text": request.document_text,
        "analysis_type": request.analysis_type,
        "specific_sections": request.specific_sections
    }
    
    background_tasks.add_task(process_document_analysis_task, task_id, inputs)
    
    return TaskResponse(
        task_id=task_id,
        status="pending",
        message="Document submitted for analysis"
    )

@app.post("/api/upload-document", response_model=TaskResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """Upload and analyze a document file"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Service not ready. Orchestrator not initialized.")
    
    task_id = str(uuid.uuid4())
    
    # Read file content
    content = await file.read()
    document_text = content.decode('utf-8', errors='ignore')
    
    task_store[task_id] = {
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "type": "document_upload",
        "filename": file.filename
    }
    
    inputs = {
        "document_text": document_text,
        "analysis_type": "comprehensive",
        "filename": file.filename
    }
    
    background_tasks.add_task(process_document_analysis_task, task_id, inputs)
    
    return TaskResponse(
        task_id=task_id,
        status="pending",
        message=f"Document '{file.filename}' uploaded for analysis"
    )

@app.post("/api/client-intake", response_model=TaskResponse)
async def client_intake(request: ClientIntakeRequest, background_tasks: BackgroundTasks):
    """Process new client intake"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Service not ready. Orchestrator not initialized.")
    
    task_id = str(uuid.uuid4())
    
    task_store[task_id] = {
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "type": "client_intake"
    }
    
    inputs = {
        "client_name": request.client_name,
        "case_description": request.case_description,
        "case_type": request.case_type,
        "jurisdiction": request.jurisdiction,
        "preferred_outcome": request.preferred_outcome,
        "budget_range": request.budget_range,
        "timeline": request.timeline
    }
    
    background_tasks.add_task(process_client_intake_task, task_id, inputs)
    
    return TaskResponse(
        task_id=task_id,
        status="pending",
        message="Client intake submitted for processing"
    )

@app.get("/api/task-status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """Get the status of a submitted task"""
    if task_id not in task_store:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = task_store[task_id]
    return TaskStatusResponse(
        task_id=task_id,
        status=task["status"],
        result=task.get("result"),
        error=task.get("error"),
        created_at=task["created_at"],
        completed_at=task.get("completed_at")
    )

@app.get("/api/tasks")
async def get_all_tasks():
    """Get all tasks (for development/debugging)"""
    return {
        "tasks": [
            {
                "task_id": tid,
                "status": task["status"],
                "type": task.get("type"),
                "created_at": task["created_at"]
            }
            for tid, task in task_store.items()
        ],
        "total": len(task_store)
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "orchestrator": "ready" if orchestrator else "not ready"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)