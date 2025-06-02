# MicroSaaS 免費版快速入門指南

## 步驟 1：下載並安裝專案

### 1.1 克隆專案到本機
```bash
git clone https://github.com/3-droid/3droid_template_lite.git

cd 3droid_template_lite
```

或者

### 1.2 下載 ZIP 檔案
- 點擊 GitHub 頁面上的綠色 "Code" 按鈕
- 選擇 "Download ZIP"
- 解壓縮到您想要的資料夾
- 開啟終端機並進入專案目錄：
  ```bash
  cd 3droid_template_lite
  ```

### 1.3 建立虛擬環境（建議）
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 1.4 安裝相依套件
```bash
pip install -r requirements.txt
```

## 步驟 2：快速體驗前端介面

### 2.1 立即啟動（無需設定）
您可以直接啟動應用程式來體驗前端介面：

```bash
streamlit run Home.py
```

> 📝 **免費版說明**：
> - 免費版主要提供前端介面體驗
> - 登入功能需要完整版才能使用
> - 您可以瀏覽所有頁面和介面設計
> - 適合了解系統架構和前端設計

## 步驟 3：客製化前端介面

### 3.1 了解 Helper 功能
開啟 `./utils/helpers.py` 了解可用的輔助函數：

- `load_style()`: 載入 CSS 樣式表
- `load_landing_page()`: 載入首頁 HTML 內容  
- `load_footer()`: 載入頁尾 HTML 內容
- `generate_navbar()`: 動態生成導航欄

### 3.2 客製化網頁內容的兩種方式

#### 方式一：直接編輯 HTML 檔案（適合開發者）
1. 進入 `template/static_html_version/` 資料夾
2. 修改相關 HTML 檔案：
   - `landing.html`：首頁內容
   - `navbar.html`：導航欄
   - `footer.html`：頁尾
   - `styles.html`：樣式設定

#### 方式二：使用網頁編輯器（推薦給非技術人員）
1. 執行編輯器：
   ```bash
   streamlit run tools/config_editor.py
   ```
2. 使用圖形化介面修改內容
3. 編輯器修改的是 `template/config/` 資料夾中的 YAML 配置檔案：
   - `auth.yaml`：登入頁面、導航欄、頁尾設定
   - `landing.yaml`：首頁內容設定   

### 3.3 切換顯示模式
在 `helpers.py` 中修改顯示模式：
```python
# 設定是否使用模板模式 (True 使用模板, False 使用靜態HTML)
_USE_TEMPLATE = True  # 預設為 True，使用方法二編輯器修改的結果
```

> 📝 **運作原理說明**：
> - **方式一 (`_USE_TEMPLATE = False`)**：
>   - 直接讀取 `template/static_html_version/` 中的靜態 HTML 檔案
>   - 適合熟悉 HTML/CSS 的開發者直接編輯
> 
> - **方式二 (`_USE_TEMPLATE = True`)**：
>   - 讀取 `template/template_version/` 中的 HTML 模板檔案
>   - 同時載入 `template/config/` 中對應的 YAML 配置檔案
>   - 使用 Jinja2 模板引擎將配置內容渲染到 HTML 模板中
>   - 適合非技術人員透過編輯器修改配置檔案
> 
> - **預設設定**：`_USE_TEMPLATE = True`，讓用戶可以直接使用圖形化編輯器
