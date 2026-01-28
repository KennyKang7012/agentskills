# 外部伺服器對接：API 整合需求建議書 (Requirement Suggestion)

## 1. 需求背景與目標
為了實現系統間的自動化協作，本建議書旨在規劃「伺服器 A」如何與「FA 報告優化平台」進行高效、穩定的垂直整合，減少人工干預，實現報告優化的自動化流水線。

## 2. 功能需求建議 (Functional Requirements)

### 2.1 身份驗證機制 (Authentication)
- **建議方案**: 使用 API Key (靜態金鑰) 並承載於 HTTP Header (`X-API-Key`)。
- **目的**: 確保只有授權的伺服器 A 可以發起優化請求，防止 API 暴露於公網造成的濫用。

### 2.2 任務啟動與檔案交換
- **上傳接口**: 提供 `multipart/form-data` 標準接口。
- **必要字段**: 原始報告 (.pptx)、評核 JSON (.json)。
- **可選字段**: AI 指示提示詞 (Prompt)，用於微調優化邏輯。

### 2.3 結果獲取模式 (Integration Patterns)
我們建議評估以下兩種模式：
- **模式 A (同步等待)**: 伺服器 A 發起請求後保持連線，直到優化完成回傳結果標識。 (目前系統已支援)
- **模式 B (異步回調/Webhook)**: 優化完成後由本平台主動通知伺服器 A。 (建議長期優化方向)

---

## 3. 非功能需求建議 (Non-Functional Requirements)

### 3.1 系統安全性 (Security)
- **傳輸加密**: 全程使用 HTTPS 協議。
- **來源限制**: 實作 IP 白名單 (IP Whitelisting)，僅允許伺服器 A 的 IP 進行呼叫。
- **檔案清理**: 建議在處理完畢並交付後的 24 小時內自動清理 `uploads/` 中的暫存檔。

### 3.2 系統健壯性 (Reliability)
- **錯誤代碼一致性**: 統一 API 的錯誤格式，針對不同場景（如 JSON 損壞、PPT 轉換失敗、LLM 超時）提供具體的 Error Code。
- **重試機制**: 伺服器 A 應具備指數退避 (Exponential Backoff) 的重試邏輯，以應對偶發的網絡連線異常。

### 3.3 監控與日誌 (Observability)
- **呼叫追蹤**: 每個請求應帶有一個 Unique Request ID，便於跨系統日誌追蹤。
- **配額限制 (Rate Limiting)**: 為保護 LLM 資源，建議設定每分鐘最大呼叫頻次。

---

## 4. 具體實作建議 (Roadmap)

1.  **Phase 1 (快速對接)**: 沿用現行 `/api/upload` 接口，增加 API Key 校驗，伺服器 A 採用同步方式調用。
2.  **Phase 2 (UX 最佳化)**: 實作 Webhook 機制，當報告產出後，本平台向伺服器 A 的預設 Endpoint 發送通知，避免長時間 HTTP 同步掛起。
