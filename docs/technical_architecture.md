# 技術架構文件

## 概述
本專案採用 **Agent Skill 模式 (Agent Skill Pattern)**，將 Web UI (Agent 介面) 與實際功能實作 (Skills) 進行分離。

## 系統架構

```mermaid
graph TD
    A[Web UI (FastAPI)] -->|觸發| B[技能管理器 Skill Manager]
    B -->|監控| C[技能進程 Skill Process]
    C -->|使用| D[技能虛擬環境 Skill Virtual Env]
    
    subgraph "應用層 Application Layer"
        A
        B
    end
    
    subgraph "技能層 Skill Layer"
        C
        D
        E[腳本與資源 Scripts & Resources]
    end
```

## 目錄結構與虛擬環境策略

我們採用 **分散式虛擬環境策略 (Distributed Virtual Environment Strategy)** 以確保技能的隔離性與移植性。

```text
專案根目錄 (agentskills)
├── app/ (Web UI)
│   ├── requirements.txt      # Web 伺服器依賴 (fastapi, uvicorn)
│   └── venv/                 # (可選) Web UI 專用環境
│
└── .agent/skills/ (技能倉庫)
    ├── fa-report-improvement/
    │   ├── requirements.txt  # 技能依賴 (python-pptx, pillow)
    │   ├── scripts/          # 實作邏輯
    │   └── venv/             # [關鍵] 技能專屬隔離環境
    │
    └── future-skill-xyz/
        ├── requirements.txt
        └── venv/             # 另一個技能的獨立環境
```

### 為什麼採用此策略？

1.  **依賴隔離 (Dependency Isolation)**：每個技能自行管理依賴。更新某個技能的函式庫不會破壞其他技能。
2.  **移植性 (Portability)**：技能是自包含單元。您可以將技能資料夾複製到另一台機器，執行安裝腳本即可運作。
3.  **整潔架構 (Clean Architecture)**：Web UI 僅作為薄封裝/協調者 (Thin Wrapper/Orchestrator)，而非龐大的依賴容器。

## 設定

環境變數透過專案根目錄下的 `.env` 檔案進行管理。

### LLM 設定
- `OPENAI_API_KEY`: LLM 服務的 API 金鑰
- `OPENAI_API_BASE`: LLM API 的基礎 URL
- `OPENAI_MODEL`: 模型部署名稱 (例如：gpt-oss-20b)

### 技能設定
- `SKILL_PATH`: 目標技能目錄的相對或絕對路徑
