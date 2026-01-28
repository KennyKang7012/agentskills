from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks
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
    report: UploadFile = File(...), 
    evaluation_json: UploadFile = File(...),
    prompt: str = Form(None)
):
    report_path = os.path.join(UPLOAD_DIR, report.filename)
    json_path = os.path.join(UPLOAD_DIR, evaluation_json.filename)
    
    with open(report_path, "wb") as buffer:
        shutil.copyfileobj(report.file, buffer)
        
    with open(json_path, "wb") as buffer:
        shutil.copyfileobj(evaluation_json.file, buffer)
    
    import time
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(report.filename)[0]
    output_filename = f"{base_name}_improved_{timestamp}.pptx"
    
    output_path = os.path.join(UPLOAD_DIR, output_filename)
    
    # 改為同步等待，確保前端能等到結果
    success, message = await process_report_task(report_path, json_path, output_path, prompt)
    
    if success:
        return {"status": "completed", "output_file": output_filename}
    else:
        # 針對常見錯誤進行分類提示
        error_type = "處理失敗"
        if "JSON" in message or "json" in message.lower():
            error_type = "JSON 格式錯誤"
        elif "ppt" in message.lower():
            error_type = "PPT 轉換/處理失敗"
            
        return {
            "status": "error", 
            "error_type": error_type,
            "message": message
        }

import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ... (router definition)

async def process_report_task(report_path: str, json_path: str, output_path: str, prompt: str = None):
    final_json_path = json_path
    logger.info(f"Starting processing for {report_path}")
    
    # 如果有提示詞，啟動 LLM 加工
    if prompt and prompt.strip():
        logger.info(f"啟動 AI 加工模式，提示詞: {prompt}")
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                original_json_data = json.load(f)
            
            success, refined_data = await llm_client.refine_evaluation_json(original_json_data, prompt)
            if success:
                refined_json_path = json_path.replace(".json", "_refined.json")
                with open(refined_json_path, "w", encoding="utf-8") as f:
                    json.dump(refined_data, f, ensure_ascii=False, indent=2)
                final_json_path = refined_json_path
                logger.info("AI 加工完成")
            else:
                logger.error(f"AI 加工失敗: {refined_data}")
                # 失敗時退回到原始 JSON
        except Exception as e:
            logger.error(f"AI 加工過程發生異常: {e}")

    logger.info(f"Calling skill manager with: {final_json_path}")
    return skill_manager.run_improvement(report_path, final_json_path, output_path)

from fastapi.responses import FileResponse

@router.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    return {"error": "File not found"}
