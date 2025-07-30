# 智慧停車場管理系統

這是一個基於 Flask 的智慧停車場管理系統，提供停車位預訂和管理功能。

## 功能特點

- 用戶管理
  - 用戶註冊和登入
  - 管理員權限控制
  - 密碼強度驗證

- 停車位管理
  - 即時停車位狀態顯示
  - 停車位預訂
  - 停車位維護管理

- 預訂系統
  - 線上預訂停車位
  - 預訂狀態追蹤
  - 預訂取消功能

- 付款系統
  - 自動計算停車費用
  - 付款狀態追蹤
  - 收據生成

- 管理功能
  - 停車位使用統計
  - 收入報表
  - 用戶管理
  - 系統日誌

## 技術架構

- 後端：Flask
- 資料庫：SQLite
- 前端：HTML, CSS, JavaScript
- 安全性：Flask-Login, Flask-WTF, Flask-Talisman
- 其他：Flask-SQLAlchemy, Flask-Limiter

## 安裝說明

1. 克隆專案
```bash
git clone https://github.com/exe5102/parkingLot.git
cd parking-lot
```

2. 建立虛擬環境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安裝依賴
```bash
pip install -r requirements.txt
```

4. 設定環境變數
```bash
cp .env.example .env
# 編輯 .env 檔案設定必要的環境變數
```

5. 初始化資料庫
```bash
flask db upgrade
```

6. 運行應用
```bash
flask run
```

## 環境變數

- `FLASK_ENV`: 運行環境 (development/production)
- `SECRET_KEY`: 應用程式密鑰
- `DATABASE_URL`: 資料庫連接字串
- `PARKING_RATE`: 每小時停車費率
- `MAX_BOOKING_HOURS`: 最大預訂時數

## 專案結構

```
parking-lot/
├── app.py              # 應用程式入口
├── config.py           # 配置檔案
├── utils.py            # 工具函數
├── requirements.txt    # 依賴套件
├── routes/            # 路由模組
│   ├── auth.py        # 認證路由
│   ├── admin.py       # 管理路由
│   └── customer.py    # 客戶路由
├── templates/         # 模板檔案
├── static/           # 靜態檔案
└── logs/             # 日誌檔案
```

## 安全性考慮

- 使用 HTTPS
- CSRF 保護
- XSS 防護
- SQL 注入防護
- 密碼加密存儲
- 請求速率限制
- 安全性標頭

## 開發指南

1. 遵循 PEP 8 程式碼風格
2. 使用類型提示
3. 編寫單元測試
4. 保持程式碼文檔更新
5. 使用 Git 分支管理

## 貢獻指南

1. Fork 專案
2. 建立功能分支
3. 提交變更
4. 發起 Pull Request

## 授權

本專案採用 MIT 授權條款。詳見 [LICENSE](LICENSE) 檔案。
