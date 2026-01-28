import httpx
import os
import asyncio

# 設定測試參數
BASE_URL = "http://localhost:8001/api"
API_KEY = "agent-skills-secret-2026"

async def test_upload_without_key():
    print("\n>>> 開始測試 1: 不帶 API Key")
    url = f"{BASE_URL}/upload"
    files = {
        'report': ('test.pptx', b'fake pptx content'),
        'evaluation_json': ('eval.json', b'{"test": "data"}')
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, files=files)
        print(f"TEST 1 狀態碼: {response.status_code}")
        # assert response.status_code == 403

async def test_upload_with_correct_key():
    print("\n>>> 開始測試 2: 帶正確 API Key")
    url = f"{BASE_URL}/upload"
    headers = {"X-API-Key": API_KEY}
    files = {
        'report': ('test.pptx', b'fake pptx content'),
        'evaluation_json': ('eval.json', b'{"test": "data"}')
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, files=files, headers=headers)
        print(f"TEST 2 狀態碼: {response.status_code}")

async def test_upload_direct():
    print("\n>>> 開始測試 3: 一步到位直接下載 (/api/upload-direct)")
    url = f"{BASE_URL}/upload-direct"
    headers = {"X-API-Key": API_KEY}
    
    report_file = "LGD Bolan  FA report Touch no function issue 1021_YM.ppt"
    json_file = "_summary_gpt-oss120b.json"
    
    if not os.path.exists(report_file) or not os.path.exists(json_file):
        print("⚠️ 找不到真實測試檔案，跳過全流程測試。")
        return

    print(f"[*] 讀取檔案: {report_file} ...")
    files = {
        'report': (report_file, open(report_file, 'rb')),
        'evaluation_json': (json_file, open(json_file, 'rb'))
    }
    
    print("[*] 正在發送請求並執行 AI 優化 (此過程約需 15-30 秒，請稍候)...")
    async with httpx.AsyncClient() as client:
        try:
            # 增加 timeout 因為處理檔案需要時間
            response = await client.post(url, files=files, headers=headers, timeout=90.0)
            print(f"[*] 伺服器響應狀態碼: {response.status_code}")
            
            if response.status_code == 200:
                content_type = response.headers.get("content-type", "")
                if "presentationml" in content_type or "application/octet-stream" in content_type:
                    with open("test_direct_download.pptx", "wb") as f:
                        f.write(response.content)
                    print(f"✅ 成功獲取檔案 (大小: {len(response.content)} bytes)")
                    print("✅ 檔案已存至: test_direct_download.pptx")
                else:
                    print(f"❌ 收到非預期內容類型: {content_type}")
                    print(f"[*] 響應內容前 200 字元: {response.text[:200]}")
            else:
                print(f"❌ 處理失敗: {response.text}")
        except httpx.TimeoutException:
            print("❌ 請求超時 (處理時間過長)")
        except Exception as e:
            print(f"❌ 發生異常: {e}")

async def main():
    await test_upload_without_key()
    await test_upload_with_correct_key()
    await test_upload_direct()
    print("\n✅ API Key 與直接下載功能測試執行完畢")

if __name__ == "__main__":
    asyncio.run(main())
