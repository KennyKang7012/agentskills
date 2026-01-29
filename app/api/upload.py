from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException, Security, Depends, status, Request
from fastapi.responses import FileResponse
import shutil
import os
import json
import time
from app.services.skill_manager import skill_manager
from app.services.llm_client import llm_client
from fastapi.security import APIKeyHeader

import logging
# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
import re

def robust_load_json(file_path: str):
    """強健地讀取 JSON 檔案，處理可能的尾隨逗號或多餘字元"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    
    # 使用 JSONDecoder 處理尾擬雜訊
    try:
        start_index = content.find('{')
        if start_index == -1:
            return json.loads(content)
            
        decoder = json.JSONDecoder()
        data, end_pos = decoder.raw_decode(content[start_index:])
        logger.info(f"DEBUG: Robust Load Success (EndPos: {end_pos}, TotalLen: {len(content)})")
        return data
    except Exception as e:
        logger.warning(f"Robust Load Failed, falling back: {e}")
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

def get_api_key(
    request: Request,
    api_key: str = Security(api_key_header)
):
    # 獲取環境變數中設定的金鑰
    expected_api_key = os.getenv("API_KEY")
    
    # 1. 如果沒設定預期金鑰，則不強制驗證 (方便本地測試)
    if not expected_api_key:
        return None
        
    # 2. 判斷來源。如果是來自同一個網域的瀏覽器請求 (Web UI)，則允許通過。
    referer = request.headers.get("referer") or ""
    host = request.headers.get("host") or ""
    
    if host and host in referer:
        return None # Web UI 請求暫時不強制要求 Header
    
    # 3. 外部伺服器 CLI 請求驗證
    if api_key == expected_api_key:
        return api_key
        
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate API Key"
    )


router = APIRouter(prefix="/api")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_report(
    report: UploadFile = File(...), 
    evaluation_json: UploadFile = File(...),
    prompt: str = Form(None),
    api_key: str = Depends(get_api_key)
):
    # 此處邏輯與 upload_direct 共享處理部分，稍後重構
    report_path, json_path, output_path, output_filename = await prepare_paths(report, evaluation_json)
    
    success, message = await process_report_task(report_path, json_path, output_path, prompt)
    
    if success:
        return {"status": "completed", "output_file": output_filename}
    else:
        return handle_error(message)

@router.post("/upload-direct")
async def upload_report_direct(
    report: UploadFile = File(...), 
    evaluation_json: UploadFile = File(...),
    prompt: str = Form(None),
    api_key: str = Depends(get_api_key)
):
    logger.info(f"API Received: {report.filename}, starting processing...")
    report_path, json_path, output_path, output_filename = await prepare_paths(report, evaluation_json)
    
    start_time = time.time()
    
    success, message = await process_report_task(report_path, json_path, output_path, prompt)
    
    elapsed = time.time() - start_time
    logger.info(f"Processing finished in {elapsed:.2f} seconds.")
    
    if success:
        if os.path.exists(output_path):
            logger.info(f"Returning file: {output_path}")
            return FileResponse(output_path, filename=output_filename, media_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
        logger.error(f"Output file missing: {output_path}")
        raise HTTPException(status_code=500, detail="Output file not found after processing")
    else:
        err = handle_error(message)
        logger.error(f"Processing failed: {err}")
        raise HTTPException(status_code=400, detail=err)

async def prepare_paths(report, evaluation_json):
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
    
    return report_path, json_path, output_path, output_filename

def handle_error(message):
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

# ... (helper functions above)

# ... (router definition)

async def process_report_task(report_path: str, json_path: str, output_path: str, prompt: str = None):
    final_json_path = json_path
    logger.info(f"Starting processing for {report_path}")
    
    # 如果有提示詞，啟動 LLM 加工
    if prompt and prompt.strip():
        logger.info(f"啟動 AI 加工模式，提示詞: {prompt}")
        try:
            original_json_data = robust_load_json(json_path)
            
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

@router.get("/skills")
async def list_skills(api_key: str = Depends(get_api_key)):
    from app.services.skill_manager import skill_registry
    return skill_registry.list_skills()

@router.get("/skills/{skill_id}")
async def get_skill_manifest(skill_id: str, api_key: str = Depends(get_api_key)):
    from app.services.skill_manager import skill_registry
    skill = skill_registry.get_skill(skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail=f"Skill '{skill_id}' not found")
    return skill.metadata

@router.get("/download/{filename}")
async def download_file(filename: str, api_key: str = Depends(get_api_key)):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename, media_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
    return {"error": "File not found"}
