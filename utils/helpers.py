import yaml
from jinja2 import Template

# 在這裡設定是否使用模板模式 (True 使用模板, False 使用靜態HTML)
_USE_TEMPLATE = True

# 根據模式決定檔案路徑前綴
_FILE_PREFIX = 'template_version' if _USE_TEMPLATE else 'static_html_version'

# 載入配置文件
def load_config(config_file):
    """載入指定的配置文件"""
    if not _USE_TEMPLATE:  # 靜態模式不需要載入配置
        return {}
        
    try:
        with open(f'template/config/{config_file}.yaml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {}

def _load_html_file(file_name, config_name=None):
    """內部函數：根據當前模式載入HTML文件
    
    參數:
        file_name: 不含路徑和副檔名的文件名
        config_name: 配置文件名稱（僅模板模式使用）
    """
    file_path = f'template/{_FILE_PREFIX}/{file_name}.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if not _USE_TEMPLATE:
        return content
    else:
        config = load_config(config_name) if config_name else {}
        template = Template(content)
        return template.render(**config)

# 基本載入函數
def load_style():
    return _load_html_file('styles')

def load_login_title():
    return _load_html_file('login_title', 'auth')

def load_login_ua():
    return _load_html_file('login_ua', 'auth')

def load_privacy_policy():
    return _load_html_file('privacy_policy', 'auth')

def load_service_term():
    return _load_html_file('service_term', 'auth')

def load_landing_page():
    return _load_html_file('landing', 'landing')

def load_footer():
    return _load_html_file('footer', 'auth')

def load_pricing():
    return _load_html_file('pricing', 'pricing')

# 特殊處理的函數
def generate_navbar(membership_info):
    if not _USE_TEMPLATE:
        with open(f'template/{_FILE_PREFIX}/navbar.html') as f:
            navbar = f.read()
        if membership_info:
            for key, value in membership_info.items():
                navbar = navbar.replace(f'{{{key}}}', str(value))
        return navbar
    else:
        with open(f'template/{_FILE_PREFIX}/navbar.html', 'r', encoding='utf-8') as f:
            template_str = f.read()
        
        # 載入配置
        config = load_config('auth')
        
        # 預處理配置，替換嵌套模板字符串
        if membership_info and 'navbar' in config and 'menu_items' in config['navbar']:
            for item in config['navbar']['menu_items']:
                if item.get('type') == 'dropdown' and 'dropdown_content' in item:
                    for content in item['dropdown_content']:
                        if 'value_var' in content:                        
                            var_str = content['value_var']
                            var_name = var_str.replace('{{', '').replace('}}', '').strip()
                            
                            # 用實際值替換變數
                            if var_name in membership_info:
                                content['value'] = membership_info[var_name]
                            else:
                                content['value'] = 'N/A'
        
        # 合併會員資訊和配置
        context = {**config}
        if membership_info:
            context['membership'] = membership_info
            
        # 使用Jinja2渲染模板
        template = Template(template_str)
        return template.render(**context)
