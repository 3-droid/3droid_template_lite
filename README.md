# MicroSaaS Free Version Quick Start Guide

## Step 1: Download and Install Project

### 1.1 Clone Project to Local Machine
```bash
git clone https://github.com/3-droid/3droid_template_lite.git

cd 3droid_template_lite
```

Or

### 1.2 Download ZIP File
- Click the green "Code" button on the GitHub page
- Select "Download ZIP"
- Extract to your desired folder
- Open terminal and navigate to project directory:
  ```bash
  cd 3droid_template_lite
  ```

### 1.3 Create Virtual Environment (Recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 1.4 Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 2: Quick Experience of Frontend Interface

### 2.1 Launch Immediately (No Configuration Required)
You can directly launch the application to experience the frontend interface:

```bash
streamlit run Home.py
```

> 📝 **Free Version Description**:
> - Free version mainly provides frontend interface experience
> - Login functionality requires full version to use
> - You can browse all pages and interface design
> - Suitable for understanding system architecture and frontend design

## Step 3: Customize Frontend Interface

### 3.1 Understanding Helper Functions
Open `./utils/helpers.py` to understand available helper functions:

- `load_style()`: Load CSS stylesheet
- `load_landing_page()`: Load homepage HTML content  
- `load_footer()`: Load footer HTML content

### 3.2 Two Ways to Customize Web Content

#### Method 1: Directly Edit HTML Files (Suitable for Developers)
1. Navigate to `template/static_html_version/` folder
2. Modify related HTML files:
   - `landing.html`: Homepage content
   - `footer.html`: Footer
   - `styles.html`: Style settings

#### Method 2: Use Web Editor (Recommended for Non-Technical Personnel)
1. Run editor:
   ```bash
   streamlit run tools/config_editor.py
   ```
2. Use graphical interface to modify content
3. Editor modifies YAML configuration files in `template/config/` folder:
   - `auth.yaml`: Login page, navigation bar, footer settings
   - `landing.yaml`: Homepage content settings   

### 3.3 Switch Display Mode
Modify display mode in `helpers.py`:
```python
# Set whether to use template mode (True uses template, False uses static HTML)
_USE_TEMPLATE = True  # Default is True, uses results from method 2 editor modifications
```

> 📝 **Operating Principle Description**:
> - **Method 1 (`_USE_TEMPLATE = False`)**:
>   - Directly reads static HTML files from `template/static_html_version/`
>   - Suitable for developers familiar with HTML/CSS to edit directly
> 
> - **Method 2 (`_USE_TEMPLATE = True`)**:
>   - Reads HTML template files from `template/template_version/`
>   - Simultaneously loads corresponding YAML configuration files from `template/config/`
>   - Uses Jinja2 template engine to render configuration content into HTML templates
>   - Suitable for non-technical personnel to modify configuration files through editor
> 
> - **Default Setting**: `_USE_TEMPLATE = True`, allowing users to directly use graphical editor