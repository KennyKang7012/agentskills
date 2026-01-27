from fastapi import APIRouter, UploadFile, File, BackgroundTasks
import shutil
import os
import json
from app.services.skill_manager import skill_manager
from app.services.llm_client import llm_client

router = APIRouter(prefix="/api")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_report(
    background_tasks: BackgroundTasks, 
    report: UploadFile = File(...), 
    evaluation_json: UploadFile = File(...)
):
    report_path = os.path.join(UPLOAD_DIR, report.filename)
    json_path = os.path.join(UPLOAD_DIR, evaluation_json.filename)
    
    with open(report_path, "wb") as buffer:
        shutil.copyfileobj(report.file, buffer)
        
    with open(json_path, "wb") as buffer:
        shutil.copyfileobj(evaluation_json.file, buffer)
    
    output_filename = f"improved_{report.filename}"
    if not output_filename.endswith(".pptx"):
        output_filename = os.path.splitext(output_filename)[0] + ".pptx"
    
    output_path = os.path.join(UPLOAD_DIR, output_filename)
    
    # 執行背景任務
    background_tasks.add_task(process_report_task, report_path, json_path, output_path)
    
    return {"status": "processing", "output_file": output_filename}

async def process_report_task(report_path: str, json_path: str, output_path: str):
    success, message = skill_manager.run_improvement(report_path, json_path, output_path)
    if success:
        print(f"Success: {message}")
    else:
        print(f"Error: {message}")

from fastapi.responses import FileResponse

@router.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    return {"error": "File not found"}
