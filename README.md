# 物聯網個人專題 Django 專案

## 檔案結構

- `mysite/`：Django 專案設定
- `mainapp/`：應用程式，包含 IoT 儀表板、API、MQTT 背景接收
- `mainapp/static/mainapp/`：CSS 與 JS 靜態檔
- `mainapp/templates/mainapp/dashboard.html`：首頁模板
- `.env`：環境變數（不要推上 GitHub）
- `requirements.txt`：Python 套件依賴

## 安裝步驟

1. 建立虛擬環境

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. 建立 MySQL 資料庫

```sql
CREATE DATABASE iot_personal_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. 確認 `.env` 內容

```text
DB_HOST=100.97.224.8
DB_PORT=3306
DB_NAME=iot_personal_db
DB_USER=root
DB_PASSWORD=root123456
MQTT_HOST=100.97.224.8
MQTT_PORT=8003
DJANGO_SECRET_KEY=django-insecure-change-this
DJANGO_DEBUG=True
```

4. 生成遷移並套用

```powershell
python manage.py makemigrations
python manage.py migrate
```

5. 啟動開發伺服器

```powershell
python manage.py runserver 8001
```

## 如果要推上 GitHub

1. 建立 `git` repo：

```powershell
git init
git add .
git commit -m "Initialize IoT Django project"
```

2. 加上遠端並推送：

```powershell
git remote add origin <你的 GitHub repo URL>
git branch -M main
git push -u origin main
```

## 目前支援功能

- MQTT 背景線程訂閱 3 個 Topic
- MySQL 儲存感測器資料
- 即時數值 AJAX 輪詢
- Chart.js 歷史折線圖
- 原始紀錄表格查詢與分頁

## 注意

- `.env` 請不要上傳
- `DEBUG=True` 只適用於開發階段
- 若部署在樹莓派，`DB_HOST` 可改為 `127.0.0.1`
