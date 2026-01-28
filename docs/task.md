# 任務：設計並規劃整合技能包的 FastAPI 網頁應用程式

- [x] 初步研究與分析 [/]
    - [x] 研究現有技能包 `.agent/skills/fa-report-improvement` [ ]
    - [x] 研究參考文件 URL [ ]
- [x] 撰寫需求文件 [ ]
    - [x] 在 `docs/` 中撰寫軟體需求文件 (PRD) [ ]
- [x] 實作計畫 [ ]
    - [x] 建立實作計畫實體文件 (Implementation Plan) [ ]
    - [x] 初始化開發環境 (uv, FastAPI) [ ]
- [x] 驗證與交付 [ ]
    - [x] 撰寫測試與驗證文件 (walkthrough.md) [ ]
    - [x] 撰寫專案 README.md [ ]
    - [x] 最終文件審閱 [ ]

- [x] Phase 2: 全自動化與提示詞觸發功能 [x]
    - [x] 更新 PRD 與實作計畫 (雙文件 + 提示詞) [x]
    - [x] 實作前端 UI 改版 (增加 Prompt 輸入框) [x]
    - [x] 實作後端 LLM 處理邏輯 (JSON 內容修飾) [x]
    - [x] 整合背景處理工作流 [x]
    - [x] 最終驗證與提交 [x]

- [x] Phase 3: 技能包升級與環境標準化 [x]
    - [x] 升級技能包至 v2.1.0 (支援 JSON Array/Object) [x]
    - [x] 實作跨平台支援 (Windows/Mac 路徑自動偵測) [x]
    - [x] 遷移至 `uv` 專案管理模式 [x]
    - [x] 建立技術架構文件 (docs/technical_architecture.md) [x]

- [x] System Testing & UX Polish [x]
    - [x] 驗證 Ollama (llama3.1) 支援 [x]
    - [x] 修復 Windows 編碼問題 (UTF-8 Stdout) [x]
    - [x] 優化使用者體驗 (同步等待模式) [x]
    - [x] 自定義輸出檔名 (時間戳記) [x]

- [x] Phase 4: 系統健壯性與韌體優化 (v2.1.3) [x]
    - [x] [腳本] 實作 JSON 自動容錯解析邏輯 [x]
    - [x] [API] 強化錯誤捕捉並傳回具體 stderr 至 UI [x]
    - [x] [UI] 增加前端 JSON 語法預檢功能 [x]
    - [x] [文件] 全面版本號同步與發布紀錄 [x]

---

# FA 報告優化專案任務清單 (繁體中文版)

- [x] **技能包更新 (v2.1.0)**
    - [x] 支援雙 JSON 格式 (陣列/物件)
    - [x] 修正 Python 腳本語法錯誤
    - [x] 更新文件 (README, SKILL.md)
    - [x] 配置 .gitignore

- [x] **Web UI 優化**
    - [x] 跨平台路徑支援 (Windows/Mac)
    - [x] 虛擬環境自動偵測
    - [x] 改善日誌紀錄與錯誤處理
    - [x] 透過環境變數配置 AI 模型

- [x] **環境架設與遷移 (uv)**
    - [x] 根據範例建立 `.env`
    - [x] 遷移至 `uv` 套件管理器
    - [x] 同步相依項目 (`uv sync`, `uv.lock`)
    - [x] 移除舊有配置 (`app/requirements.txt`)

- [x] **系統測試與體驗磨光**
    - [x] 修正 Windows Unicode/編碼問題 (UTF-8)
    - [x] 實作同步報告處理流程 (優化 UX)
    - [x] 帶有時間戳記的輸出檔名 (`_improved_TIMESTAMP.pptx`)
    - [x] 精煉文件 (PRD/README/技能文件)
    - [x] Git 提交與版本同步 (v2.1.2)

- [x] **Phase 4: 系統健壯性與韌體優化 (v2.1.3)**
    - [x] [腳本] 實作 JSON 清洗器 (基於正則表達式的自動修補)
    - [x] [API] 強化錯誤捕捉 (將詳細 stderr 傳回 UI)
    - [x] [UI] 增加前端 JSON 語法預檢與智慧修復功能
    - [x] [文件] 全面版本號同步與發布紀錄 [x]
    - [x] [驗證] 透過 Web UI 與 Coding Agent 完成全棧驗證
