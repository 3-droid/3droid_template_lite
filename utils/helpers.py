import yaml
from jinja2 import Template

# Set whether to use template mode (True for template, False for static HTML)
_USE_TEMPLATE = True

# Determine file path prefix based on mode
_FILE_PREFIX = 'template_version' if _USE_TEMPLATE else 'static_html_version'

# Load configuration file
def load_config(config_file):
    """Load the specified configuration file"""
    if not _USE_TEMPLATE:
        return {}
        
    try:
        with open(f'template/config/{config_file}.yaml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {}

def _load_html_file(file_name, config_name=None):
    """Internal function: Load HTML file based on current mode
    
    Parameters:
        file_name: File name without path and extension
        config_name: Configuration file name (used only in template mode)
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

# Basic loading functions
def load_style():
    return _load_html_file('styles')

def load_landing_page():
    return _load_html_file('landing', 'landing')

def load_footer():
    return _load_html_file('footer', 'auth')

