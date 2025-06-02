import streamlit as st
import yaml
import os
from typing import Dict, Any

# 設置頁面標題和佈局
st.set_page_config(page_title="網站配置編輯器", layout="wide")

def load_config() -> Dict[str, Any]:
    """載入配置檔案"""
    try:
        with open("template/config/landing.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        # 如果檔案不存在，返回空字典
        return {}

def save_config(config: Dict[str, Any]) -> None:
    """儲存配置檔案"""
    # 確保目錄存在
    os.makedirs("template/config", exist_ok=True)
    with open("template/config/landing.yaml", "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)

def load_auth_config() -> Dict[str, Any]:
    """載入 auth.yaml 配置檔案"""
    try:
        with open("template/config/auth.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        # 如果檔案不存在，返回空字典
        return {}

def save_auth_config(config: Dict[str, Any]) -> None:
    """儲存 auth.yaml 配置檔案"""
    # 確保目錄存在
    os.makedirs("template/config", exist_ok=True)
    with open("template/config/auth.yaml", "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)

config_type = st.sidebar.radio(
    "選擇配置檔案",
    ["主頁配置 (landing.yaml)", "登入頁配置 (auth.yaml)"]
)

# 載入現有配置
config = load_config()
if not config:
    config = {"landing": {}}

landing_config = config.get("landing", {})

auth_config = load_auth_config()
if not auth_config:
    auth_config = {}


# 根據選擇載入相應的配置
if config_type == "主頁配置 (landing.yaml)":
    # 標題
    st.title("網站配置編輯器")
    st.markdown("透過此表單修改網站的內容和外觀，修改完成後點擊底部的「儲存變更」按鈕。")

    # 使用標籤頁來組織不同區域的設定
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["封面區", "服務特色", "體驗Demo", "價格方案", "常見問題"])

    # 封面區設定
    with tab1:
        st.header("封面區設定")
        
        hero_config = landing_config.get("hero", {})
        
        # 標題
        hero_heading = st.text_area(
            "標題文字", 
            value=hero_config.get("heading", "輕鬆建立輕量級軟體服務<br>Micro SaaS"),
            help="可使用 <br> 來換行"
        )
        
        # CTA按鈕文字
        hero_cta_text = st.text_input(
            "按鈕文字",
            value=hero_config.get("cta_button", {}).get("text", "立即體驗")
        )
        
        # 影片來源 (可選)
        hero_video_source = st.text_input(
            "影片來源 URL",
            value=hero_config.get("video", {}).get("source", "")
        )
        
        # 更新配置
        if "hero" not in landing_config:
            landing_config["hero"] = {}
        
        landing_config["hero"]["section_id"] = "home"  # 固定值
        landing_config["hero"]["heading"] = hero_heading
        
        if "cta_button" not in landing_config["hero"]:
            landing_config["hero"]["cta_button"] = {}
        
        landing_config["hero"]["cta_button"]["text"] = hero_cta_text
        landing_config["hero"]["cta_button"]["link"] = "/app"  # 固定值
        landing_config["hero"]["cta_button"]["icon"] = "bi bi-chevron-right"  # 固定值
        
        if hero_video_source:
            if "video" not in landing_config["hero"]:
                landing_config["hero"]["video"] = {}
            landing_config["hero"]["video"]["source"] = hero_video_source
            landing_config["hero"]["video"]["type"] = "video/mp4"  # 固定值

    # 服務特色設定
    with tab2:
        st.header("服務特色設定")
        
        feature_config = landing_config.get("feature", {})
        
        # 標題和副標題
        feature_title = st.text_input(
            "標題",
            value=feature_config.get("title", "服務特色")
        )
        
        feature_subtitle = st.text_input(
            "副標題",
            value=feature_config.get("subtitle", "結合專業工具，一站式解決方案")
        )
        
        # 特色項目
        st.subheader("特色項目")
        
        # 初始化 session_state 來存儲特色項目
        if "feature_items" not in st.session_state:
            feature_items = feature_config.get("list_item", [])
            
            # 確保至少有一個項目
            if not feature_items:
                feature_items = [{
                    "column_width": "4",
                    "icon_url": "",
                    "icon_alt": "",
                    "title": "",
                    "description": ""
                }]
            
            st.session_state.feature_items = feature_items
        
        # 新增特色項目的函數
        def add_feature_item():
            st.session_state.feature_items.append({
                "column_width": "4",
                "icon_url": "",
                "icon_alt": "",
                "title": "",
                "description": ""
            })
        
        # 刪除特色項目的函數
        def delete_last_feature_item():
            if len(st.session_state.feature_items) > 1:
                st.session_state.feature_items.pop()
        
        # 動態生成特色項目編輯區
        updated_feature_items = []
        
        for i, item in enumerate(st.session_state.feature_items):
            st.markdown(f"#### 項目 {i+1}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input(
                    f"標題 #{i+1}", 
                    value=item.get("title", ""),
                    key=f"feature_title_{i}"
                )
                icon_url = st.text_input(
                    f"圖示URL #{i+1}", 
                    value=item.get("icon_url", ""),
                    key=f"feature_icon_url_{i}"
                )
                icon_alt = st.text_input(
                    f"圖示替代文字 #{i+1}", 
                    value=item.get("icon_alt", ""),
                    key=f"feature_icon_alt_{i}"
                )
            
            with col2:
                column_width = st.select_slider(
                    f"欄寬 #{i+1}",
                    options=["4", "5", "6", "7", "8"],
                    value=item.get("column_width", "4"),
                    key=f"feature_column_width_{i}"
                )
                description = st.text_area(
                    f"描述 #{i+1}", 
                    value=item.get("description", ""),
                    key=f"feature_description_{i}"
                )
            
            updated_feature_items.append({
                "column_width": column_width,
                "icon_url": icon_url,
                "icon_alt": icon_alt,
                "title": title,
                "description": description
            })
            
            if i < len(st.session_state.feature_items) - 1:
                st.markdown("---")
        
        # 更新 session_state 中的特色項目
        st.session_state.feature_items = updated_feature_items
        
        # 新增/刪除項目的按鈕
        col1, col2 = st.columns(2)
        
        with col1:
            st.button("➕ 新增特色項目", on_click=add_feature_item, key="add_feature_item")
        
        with col2:
            st.button("➖ 刪除最後一個項目", 
                    on_click=delete_last_feature_item, 
                    disabled=len(st.session_state.feature_items) <= 1,
                    key="delete_feature_item")
        
        # 更新配置
        if "feature" not in landing_config:
            landing_config["feature"] = {}
        
        landing_config["feature"]["section_id"] = "feature"  # 固定值
        landing_config["feature"]["title"] = feature_title
        landing_config["feature"]["subtitle"] = feature_subtitle
        landing_config["feature"]["list_item"] = st.session_state.feature_items


    # 體驗Demo設定    
    with tab3:
        st.header("體驗Demo設定")
        
        demo_config = landing_config.get("demo", {})
        
        # 標題和主標題
        demo_heading = st.text_area(
            "標題",
            value=demo_config.get("heading", "Streamlit+ AI 驅動<br>快速生成器"),
            help="可使用 <br> 來換行"
        )
        
        demo_main_title = st.text_input(
            "主標題",
            value=demo_config.get("main_title", "專注於開發您的 Streamlit 應用，會員管理與金流就交給我們！")
        )
        
        # 圖片設定
        demo_image_src = st.text_input(
            "圖片來源",
            value=demo_config.get("image", {}).get("src", "app/static/cycles.webp")
        )
        
        # 優勢項目
        st.subheader("優勢項目")
        
        # 初始化 session_state 來存儲優勢項目
        if "demo_benefits" not in st.session_state:
            benefits = demo_config.get("benefits", [])
            
            # 確保至少有一個項目
            if not benefits:
                benefits = [{
                    "icon_class": "fas fa-robot",
                    "title": "",
                    "description": ""
                }]
            
            st.session_state.demo_benefits = benefits
        
        # 新增優勢項目的函數
        def add_benefit():
            st.session_state.demo_benefits.append({
                "icon_class": "fas fa-star",
                "title": "",
                "description": ""
            })
        
        # 刪除優勢項目的函數
        def delete_last_benefit():
            if len(st.session_state.demo_benefits) > 1:
                st.session_state.demo_benefits.pop()
        
        # 動態生成優勢項目編輯區
        updated_benefits = []
        
        for i, benefit in enumerate(st.session_state.demo_benefits):
            st.markdown(f"#### 優勢 {i+1}")
            
            icon_class = st.text_input(
                f"圖示類別 #{i+1}", 
                value=benefit.get("icon_class", "fas fa-robot"),
                help="使用 Font Awesome 圖示類別，例如 fas fa-robot",
                key=f"benefit_icon_class_{i}"
            )
            
            title = st.text_input(
                f"標題 #{i+1}", 
                value=benefit.get("title", ""),
                key=f"benefit_title_{i}"
            )
            description = st.text_area(
                f"描述 #{i+1}", 
                value=benefit.get("description", ""),
                key=f"benefit_description_{i}"
            )
            
            updated_benefits.append({
                "icon_class": icon_class,
                "title": title,
                "description": description
            })
            
            if i < len(st.session_state.demo_benefits) - 1:
                st.markdown("---")
        
        # 更新 session_state 中的優勢項目
        st.session_state.demo_benefits = updated_benefits
        
        # 新增/刪除優勢的按鈕
        col1, col2 = st.columns(2)
        
        with col1:
            st.button("➕ 新增優勢項目", on_click=add_benefit, key="add_benefit")
        
        with col2:
            st.button("➖ 刪除最後一個優勢", 
                    on_click=delete_last_benefit, 
                    disabled=len(st.session_state.demo_benefits) <= 1,
                    key="delete_benefit")
        
        # CTA按鈕
        st.subheader("CTA按鈕")
        
        # 初始化 session_state 來存儲CTA按鈕
        if "cta_buttons" not in st.session_state:
            cta_buttons = demo_config.get("cta_buttons", [])
            
            # 確保至少有一個按鈕
            if not cta_buttons:
                cta_buttons = [{
                    "class": "cta-button white",
                    "link": "/app",
                    "icon": "bi bi-magic",
                    "text": "試用AI生成器"
                }]
            
            st.session_state.cta_buttons = cta_buttons
        
        # 新增CTA按鈕的函數
        def add_cta_button():
            st.session_state.cta_buttons.append({
                "class": "cta-button-class",
                "link": "/app",
                "text": "新按鈕"
            })
        
        # 刪除CTA按鈕的函數
        def delete_last_cta_button():
            if len(st.session_state.cta_buttons) > 1:
                st.session_state.cta_buttons.pop()
        
        # 動態生成按鈕編輯區
        updated_cta_buttons = []
        
        for i, button in enumerate(st.session_state.cta_buttons):
            st.markdown(f"#### 按鈕 {i+1}")
            
            text = st.text_input(
                f"按鈕文字 #{i+1}", 
                value=button.get("text", ""),
                key=f"cta_text_{i}"
            )
            link = st.text_input(
                f"連結 #{i+1}", 
                value=button.get("link", "/app"),
                key=f"cta_link_{i}"
            )
            
            # 可選項
            icon = st.text_input(
                f"圖示 (可選) #{i+1}", 
                value=button.get("icon", ""),
                help="使用 Bootstrap Icons 類別，例如 bi bi-magic",
                key=f"cta_icon_{i}"
            )
            
            button_class = st.text_input(
                f"CSS類別 #{i+1}", 
                value=button.get("class", "cta-button white"),
                help="按鈕的CSS類別，例如 cta-button white",
                key=f"cta_class_{i}"
            )
            
            button_data = {
                "class": button_class,
                "link": link,
                "text": text
            }
            
            if icon:
                button_data["icon"] = icon
                
            updated_cta_buttons.append(button_data)
            
            if i < len(st.session_state.cta_buttons) - 1:
                st.markdown("---")
        
        # 更新 session_state 中的CTA按鈕
        st.session_state.cta_buttons = updated_cta_buttons
        
        # 新增/刪除按鈕的按鈕
        col1, col2 = st.columns(2)
        
        with col1:
            st.button("➕ 新增按鈕", on_click=add_cta_button, key="add_cta_button")
        
        with col2:
            st.button("➖ 刪除最後一個按鈕", 
                    on_click=delete_last_cta_button, 
                    disabled=len(st.session_state.cta_buttons) <= 1,
                    key="delete_cta_button")
        
        # 更新配置
        if "demo" not in landing_config:
            landing_config["demo"] = {}
        
        landing_config["demo"]["section_id"] = "demo"  # 固定值
        landing_config["demo"]["heading"] = demo_heading
        landing_config["demo"]["main_title"] = demo_main_title
        
        if "image" not in landing_config["demo"]:
            landing_config["demo"]["image"] = {}
        
        landing_config["demo"]["image"]["src"] = demo_image_src
        landing_config["demo"]["image"]["height"] = "1028"  # 固定值
        landing_config["demo"]["image"]["width"] = "2168"  # 固定值
        
        landing_config["demo"]["benefits"] = st.session_state.demo_benefits
        landing_config["demo"]["cta_buttons"] = st.session_state.cta_buttons


    # 價格方案設定
    with tab4:
        st.header("價格方案設定")
        
        pricing_config = landing_config.get("pricing", {})
        
        # 標題
        pricing_title = st.text_input(
            "標題",
            value=pricing_config.get("title", "選擇你的方案")
        )
        
        # 方案項目
        st.subheader("方案項目")
        
        # 初始化 session_state 來存儲方案
        if "pricing_plans" not in st.session_state:
            plans = pricing_config.get("plans", [])
            
            # 確保至少有一個方案
            if not plans:
                plans = [{
                    "name": "免費版",
                    "is_popular": False,
                    "price": "$0",
                    "price_period": "/月",
                    "ai_quota": "每月 1 次 AI 生成額度",
                    "features": ["基礎版面配置範本", "社群分享功能", "基礎程式碼優化"],
                    "button": {
                        "link": "https://www.patreon.com/c/3droid/membership",
                        "class": "btn btn-outline w-100",
                        "text": "開始使用"
                    }
                }]
            
            st.session_state.pricing_plans = plans
        
        # 新增方案的函數
        def add_pricing_plan():
            st.session_state.pricing_plans.append({
                "name": "新方案",
                "is_popular": False,
                "price": "$0",
                "price_period": "/月",
                "ai_quota": "每月 AI 生成額度",
                "features": ["功能 1", "功能 2"],
                "button": {
                    "link": "#",
                    "class": "btn btn-outline w-100",
                    "text": "選擇方案"
                }
            })
        
        # 刪除方案的函數
        def delete_last_pricing_plan():
            if len(st.session_state.pricing_plans) > 1:
                st.session_state.pricing_plans.pop()
        
        # 動態生成方案編輯區
        updated_plans = []
        
        for i, plan in enumerate(st.session_state.pricing_plans):
            st.markdown(f"#### 方案 {i+1}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input(
                    f"方案名稱 #{i+1}", 
                    value=plan.get("name", ""),
                    key=f"plan_name_{i}"
                )
                price = st.text_input(
                    f"價格 #{i+1}", 
                    value=plan.get("price", "$0"),
                    key=f"plan_price_{i}"
                )
                price_period = st.text_input(
                    f"價格週期 #{i+1}", 
                    value=plan.get("price_period", "/月"),
                    key=f"plan_price_period_{i}"
                )
                ai_quota = st.text_input(
                    f"AI配額 #{i+1}", 
                    value=plan.get("ai_quota", "每月 1 次 AI 生成額度"),
                    key=f"plan_ai_quota_{i}"
                )
            
            with col2:
                is_popular = st.checkbox(
                    f"是否為熱門方案 #{i+1}", 
                    value=plan.get("is_popular", False),
                    key=f"plan_is_popular_{i}"
                )
                
                popular_badge_text = ""
                if is_popular:
                    popular_badge_text = st.text_input(
                        f"熱門標籤文字 #{i+1}", 
                        value=plan.get("popular_badge_text", "最受歡迎"),
                        key=f"plan_popular_badge_text_{i}"
                    )
            
            # 功能列表
            st.markdown(f"##### 功能列表 #{i+1}")
            
            # 初始化該方案的功能列表 session_state
            plan_features_key = f"plan_{i}_features"
            if plan_features_key not in st.session_state:
                features = plan.get("features", [])
                
                # 確保至少有一個功能
                if not features:
                    features = [""]
                
                st.session_state[plan_features_key] = features
            
            # 新增功能的函數
            def add_feature_to_plan(plan_idx):
                return lambda: st.session_state[f"plan_{plan_idx}_features"].append("")
            
            # 刪除功能的函數
            def delete_last_feature_from_plan(plan_idx):
                return lambda: st.session_state[f"plan_{plan_idx}_features"].pop() if len(st.session_state[f"plan_{plan_idx}_features"]) > 1 else None
            
            # 動態生成功能列表編輯區
            updated_features = []
            
            for j, feature in enumerate(st.session_state[plan_features_key]):
                feature_text = st.text_input(
                    f"功能 #{i+1}-{j+1}", 
                    value=feature,
                    key=f"plan_{i}_feature_{j}"
                )
                updated_features.append(feature_text)
            
            # 更新 session_state 中的功能列表
            st.session_state[plan_features_key] = updated_features
            
            # 新增/刪除功能的按鈕
            col1, col2 = st.columns(2)
            
            with col1:
                st.button(
                    f"➕ 新增功能 #{i+1}", 
                    on_click=add_feature_to_plan(i),
                    key=f"add_feature_to_plan_{i}"
                )
            
            with col2:
                st.button(
                    f"➖ 刪除最後一個功能 #{i+1}", 
                    on_click=delete_last_feature_from_plan(i),
                    disabled=len(st.session_state[plan_features_key]) <= 1,
                    key=f"delete_feature_from_plan_{i}"
                )
            
            # 按鈕設定
            st.markdown(f"##### 按鈕設定 #{i+1}")
            
            button = plan.get("button", {})
            button_text = st.text_input(
                f"按鈕文字 #{i+1}", 
                value=button.get("text", "開始使用"),
                key=f"plan_button_text_{i}"
            )
            button_link = st.text_input(
                f"按鈕連結 #{i+1}", 
                value=button.get("link", ""),
                key=f"plan_button_link_{i}"
            )
            button_class = st.text_input(
                f"按鈕CSS類別 #{i+1}", 
                value=button.get("class", "btn btn-outline w-100"),
                help="按鈕的CSS類別，例如 btn btn-outline w-100",
                key=f"plan_button_class_{i}"
            )
            
            # 構建方案數據
            plan_data = {
                "name": name,
                "is_popular": is_popular,
                "price": price,
                "price_period": price_period,
                "ai_quota": ai_quota,
                "features": st.session_state[plan_features_key],
                "button": {
                    "link": button_link,
                    "class": button_class,
                    "text": button_text
                }
            }
            
            if is_popular:
                plan_data["popular_badge_text"] = popular_badge_text
                
            updated_plans.append(plan_data)
            
            if i < len(st.session_state.pricing_plans) - 1:
                st.markdown("---")
        
        # 更新 session_state 中的方案
        st.session_state.pricing_plans = updated_plans
        
        # 新增/刪除方案的按鈕
        col1, col2 = st.columns(2)
        
        with col1:
            st.button("➕ 新增方案", on_click=add_pricing_plan, key="add_pricing_plan")
        
        with col2:
            st.button("➖ 刪除最後一個方案", 
                    on_click=delete_last_pricing_plan, 
                    disabled=len(st.session_state.pricing_plans) <= 1,
                    key="delete_pricing_plan")
        
        # 更新配置
        if "pricing" not in landing_config:
            landing_config["pricing"] = {}
        
        landing_config["pricing"]["section_id"] = "pricing"  # 固定值
        landing_config["pricing"]["title"] = pricing_title
        landing_config["pricing"]["feature_icon"] = "fas fa-check"  # 固定值
        landing_config["pricing"]["plans"] = st.session_state.pricing_plans


    # FAQ設定
    with tab5:
        st.header("常見問題設定")
        
        faq_config = landing_config.get("faq", {})
        
        # 標題
        faq_title = st.text_input(
            "標題",
            value=faq_config.get("title", "常見問題")
        )
        
        # FAQ項目
        st.subheader("FAQ項目")
        
        # 初始化 session_state 來存儲 FAQ 項目
        if "faq_items" not in st.session_state:
            faq_items = faq_config.get("faq_items", [])
            
            # 確保至少有一個FAQ項目
            if not faq_items:
                faq_items = [{
                    "question": "問題?",
                    "answer": "回答..."
                }]
            
            st.session_state.faq_items = faq_items
        
        # 新增 FAQ 項目的函數
        def add_faq_item():
            st.session_state.faq_items.append({
                "question": "",
                "answer": ""
            })
        
        # 刪除 FAQ 項目的函數
        def delete_last_faq_item():
            if len(st.session_state.faq_items) > 1:
                st.session_state.faq_items.pop()
        
        # 動態生成FAQ項目編輯區
        updated_faq_items = []
        
        for i, item in enumerate(st.session_state.faq_items):
            st.markdown(f"#### 問答 {i+1}")
            
            question = st.text_input(
                f"問題 #{i+1}", 
                value=item.get("question", ""),
                key=f"faq_question_{i}"
            )
            answer = st.text_area(
                f"回答 #{i+1}", 
                value=item.get("answer", ""),
                key=f"faq_answer_{i}"
            )
            
            updated_faq_items.append({
                "question": question,
                "answer": answer
            })
            
            if i < len(st.session_state.faq_items) - 1:
                st.markdown("---")
        
        # 更新 session_state 中的 FAQ 項目
        st.session_state.faq_items = updated_faq_items
        
        # 新增/刪除FAQ項目的按鈕
        col1, col2 = st.columns(2)
        
        with col1:
            st.button("➕ 新增FAQ項目", on_click=add_faq_item)
        
        with col2:
            st.button("➖ 刪除最後一個FAQ項目", on_click=delete_last_faq_item, 
                    disabled=len(st.session_state.faq_items) <= 1)
        
        # 更新配置
        if "faq" not in landing_config:
            landing_config["faq"] = {}
        
        landing_config["faq"]["title"] = faq_title
        landing_config["faq"]["faq_items"] = st.session_state.faq_items



    # 儲存按鈕
    if st.button("儲存變更", type="primary"):
        config["landing"] = landing_config
        save_config(config)
        st.success("配置已成功儲存！")        

    # 顯示當前配置 (僅在開發模式)
    with st.expander("查看當前配置 (YAML格式)"):
        st.code(yaml.dump(config, allow_unicode=True, sort_keys=False), language="yaml")

# 認證頁配置
else:
    st.title("認證頁配置編輯器")
    st.markdown("修改認證頁面的內容和外觀，修改完成後點擊底部的「儲存變更」按鈕。")
    
    # 使用標籤頁來組織不同區域的設定
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["頁尾設定", "登入提示", "登入標題", "隱私政策", "服務條款", "導航欄"])
    
    # 頁尾設定
    with tab1:
        st.header("頁尾設定")
        
        footer_config = auth_config.get("footer", {})
        
        # Logo 設定
        st.subheader("Logo 設定")
        logo_src = st.text_input(
            "Logo 圖片來源",
            value=footer_config.get("logo", {}).get("src", "")
        )
        logo_alt = st.text_input(
            "Logo 替代文字",
            value=footer_config.get("logo", {}).get("alt", "三卓金融科技")
        )
        
        # 社群連結
        st.subheader("社群連結")
        
        # 初始化 session_state 來存儲社群連結
        if "social_links" not in st.session_state:
            social_links = footer_config.get("social_links", [])
            if not social_links:
                social_links = []
            
            st.session_state.social_links = social_links
        
        # 新增社群連結的函數
        def add_social_link():
            st.session_state.social_links.append({
                "name": "",
                "url": "",
                "icon": ""
            })
        
        # 刪除社群連結的函數
        def delete_last_social_link():
            if len(st.session_state.social_links) > 0:
                st.session_state.social_links.pop()
        
        # 動態生成社群連結編輯區
        updated_social_links = []
        
        for i, link in enumerate(st.session_state.social_links):
            st.markdown(f"#### 連結 {i+1}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input(
                    f"平台名稱 #{i+1}", 
                    value=link.get("name", ""),
                    key=f"social_name_{i}"
                )
                icon = st.text_input(
                    f"圖示代碼 #{i+1}", 
                    value=link.get("icon", ""),
                    key=f"social_icon_{i}"
                )
            
            with col2:
                url = st.text_input(
                    f"連結網址 #{i+1}", 
                    value=link.get("url", ""),
                    key=f"social_url_{i}"
                )
            
            updated_social_links.append({
                "name": name,
                "url": url,
                "icon": icon
            })
            
            if i < len(st.session_state.social_links) - 1:
                st.markdown("---")
        
        # 更新 session_state 中的社群連結
        st.session_state.social_links = updated_social_links
        
        # 新增/刪除社群連結的按鈕
        col1, col2 = st.columns(2)
        
        with col1:
            st.button(
                "➕ 新增社群連結", 
                on_click=add_social_link,
                key="add_social_link"
            )
        
        with col2:
            st.button(
                "➖ 刪除最後一個社群連結", 
                on_click=delete_last_social_link,
                disabled=len(st.session_state.social_links) <= 0,
                key="delete_social_link"
            )
        
        # 更新配置
        if "footer" not in auth_config:
            auth_config["footer"] = {}
        
        if "logo" not in auth_config["footer"]:
            auth_config["footer"]["logo"] = {}
        
        auth_config["footer"]["logo"]["src"] = logo_src
        auth_config["footer"]["logo"]["alt"] = logo_alt
        auth_config["footer"]["social_links"] = st.session_state.social_links

    
    # 登入提示設定
    with tab2:
        st.header("登入提示設定")
        
        login_ua_config = auth_config.get("login_ua", {})
        
        agreement_text = st.text_input(
            "協議文字",
            value=login_ua_config.get("agreement_text", "登入即表示您同意我們的")
        )
        
        terms_text = st.text_input(
            "服務條款文字",
            value=login_ua_config.get("terms_text", "服務條款")
        )
        
        terms_link = st.text_input(
            "服務條款連結",
            value=login_ua_config.get("terms_link", "/service_term")
        )
        
        and_text = st.text_input(
            "連接詞",
            value=login_ua_config.get("and_text", "和")
        )
        
        privacy_text = st.text_input(
            "隱私政策文字",
            value=login_ua_config.get("privacy_text", "隱私政策")
        )
        
        privacy_link = st.text_input(
            "隱私政策連結",
            value=login_ua_config.get("privacy_link", "/privacy_policy")
        )
        
        # 更新配置
        if "login_ua" not in auth_config:
            auth_config["login_ua"] = {}
        
        auth_config["login_ua"]["agreement_text"] = agreement_text
        auth_config["login_ua"]["terms_text"] = terms_text
        auth_config["login_ua"]["terms_link"] = terms_link
        auth_config["login_ua"]["and_text"] = and_text
        auth_config["login_ua"]["privacy_text"] = privacy_text
        auth_config["login_ua"]["privacy_link"] = privacy_link
    
    # 登入標題設定
    with tab3:
        st.header("登入標題設定")
        
        login_title_config = auth_config.get("login_title", {})
        
        heading = st.text_input(
            "標題",
            value=login_title_config.get("heading", "透過 Patreon 登入，自動載入會籍")
        )
        
        description_line1 = st.text_input(
            "描述第一行",
            value=login_title_config.get("description_line1", "根據您的會籍決定每個月可以生成幾次Streamlit應用。")
        )
        
        description_line2 = st.text_input(
            "描述第二行",
            value=login_title_config.get("description_line2", "每位新用戶可每月免費體驗一次生成服務。")
        )
        
        # 更新配置
        if "login_title" not in auth_config:
            auth_config["login_title"] = {}
        
        auth_config["login_title"]["heading"] = heading
        auth_config["login_title"]["description_line1"] = description_line1
        auth_config["login_title"]["description_line2"] = description_line2

        # 隱私政策設定
    # 隱私政策設定
    with tab4:
        st.header("隱私政策設定")
        
        privacy_policy_config = auth_config.get("privacy_policy", {})
        
        title = st.text_input(
            "標題",
            value=privacy_policy_config.get("title", "隱私政策")
        )
        
        last_updated = st.text_input(
            "最後更新日期",
            value=privacy_policy_config.get("last_updated", "最後更新日期：2024年12月4日")
        )
        
        # 各區段編輯
        st.subheader("政策區段")
        
        sections = privacy_policy_config.get("sections", {})
        
        # 定義所有區段及其結構
        section_definitions = [
            {
                "key": "introduction",
                "default_title": "1. 引言",
                "has_content": True,
                "has_intro": False,
                "has_list_items": False
            },
            {
                "key": "data_collection",
                "default_title": "2. 信息收集",
                "has_content": False,
                "has_intro": True,
                "has_list_items": True
            },
            {
                "key": "data_usage",
                "default_title": "3. 信息使用",
                "has_content": False,
                "has_intro": True,
                "has_list_items": True
            },
            {
                "key": "data_sharing",
                "default_title": "4. 信息共享",
                "has_content": False,
                "has_intro": True,
                "has_list_items": True
            },
            {
                "key": "data_security",
                "default_title": "5. 數據安全",
                "has_content": True,
                "has_intro": False,
                "has_list_items": False
            },
            {
                "key": "user_rights",
                "default_title": "6. 您的權利",
                "has_content": True,
                "has_intro": False,
                "has_list_items": False
            },
            {
                "key": "changes",
                "default_title": "7. 變更",
                "has_content": True,
                "has_intro": False,
                "has_list_items": False
            },
            {
                "key": "contact",
                "default_title": "8. 聯繫我們",
                "has_content": True,
                "has_intro": False,
                "has_list_items": False
            }
        ]
        
        # 動態生成所有區段的編輯界面
        for i, section_def in enumerate(section_definitions):
            section_key = section_def["key"]
            section_data = sections.get(section_key, {})
            
            st.markdown(f"#### {section_def['default_title']}")
            
            # 標題
            section_title = st.text_input(
                f"{section_key} 標題",
                value=section_data.get("title", section_def["default_title"]),
                key=f"privacy_{section_key}_title"
            )
            
            # 內容 (如果適用)
            if section_def["has_content"]:
                section_content = st.text_area(
                    f"{section_key} 內容",
                    value=section_data.get("content", ""),
                    key=f"privacy_{section_key}_content"
                )
            
            # 介紹 (如果適用)
            if section_def["has_intro"]:
                section_intro = st.text_area(
                    f"{section_key} 介紹",
                    value=section_data.get("intro", ""),
                    key=f"privacy_{section_key}_intro"
                )
            
            # 列表項目 (如果適用)
            if section_def["has_list_items"]:
                st.markdown(f"##### {section_key} 列表項目")
                
                # 初始化 session_state 來存儲列表項目
                list_items_key = f"privacy_{section_key}_items"
                if list_items_key not in st.session_state:
                    list_items = section_data.get("list_items", [])
                    if not list_items:
                        list_items = [""]
                    st.session_state[list_items_key] = list_items
                
                # 新增列表項目的函數
                def add_list_item(section_key):
                    def _add_item():
                        st.session_state[f"privacy_{section_key}_items"].append("")
                    return _add_item
                
                # 刪除列表項目的函數
                def delete_last_list_item(section_key):
                    def _delete_item():
                        if len(st.session_state[f"privacy_{section_key}_items"]) > 1:
                            st.session_state[f"privacy_{section_key}_items"].pop()
                    return _delete_item
                
                # 顯示現有項目的輸入框
                updated_items = []
                for j, item in enumerate(st.session_state[list_items_key]):
                    item_value = st.text_input(
                        f"{section_key} 項目 #{j+1}",
                        value=item,
                        key=f"privacy_{section_key}_item_{j}"
                    )
                    updated_items.append(item_value)
                
                # 更新 session_state 中的列表項目
                st.session_state[list_items_key] = updated_items
                
                # 新增/刪除項目的按鈕
                col1, col2 = st.columns(2)
                
                with col1:
                    st.button(
                        f"➕ 新增 {section_key} 項目",
                        on_click=add_list_item(section_key),
                        key=f"add_{section_key}_item"
                    )
                
                with col2:
                    st.button(
                        f"➖ 刪除最後一個 {section_key} 項目",
                        on_click=delete_last_list_item(section_key),
                        disabled=len(st.session_state[list_items_key]) <= 1,
                        key=f"delete_{section_key}_item"
                    )
            
            # 更新配置
            if "privacy_policy" not in auth_config:
                auth_config["privacy_policy"] = {}
                
            if "sections" not in auth_config["privacy_policy"]:
                auth_config["privacy_policy"]["sections"] = {}
            
            if section_key not in auth_config["privacy_policy"]["sections"]:
                auth_config["privacy_policy"]["sections"][section_key] = {}
            
            auth_config["privacy_policy"]["sections"][section_key]["title"] = section_title
            
            if section_def["has_content"]:
                auth_config["privacy_policy"]["sections"][section_key]["content"] = section_content
            
            if section_def["has_intro"]:
                auth_config["privacy_policy"]["sections"][section_key]["intro"] = section_intro
            
            if section_def["has_list_items"]:
                auth_config["privacy_policy"]["sections"][section_key]["list_items"] = st.session_state[f"privacy_{section_key}_items"]
            
            st.markdown("---")
        
        # 返回按鈕設定
        st.subheader("返回按鈕")
        
        return_button = privacy_policy_config.get("return_button", {})
        return_link = st.text_input(
            "返回連結",
            value=return_button.get("link", "/app")
        )
        return_text = st.text_input(
            "返回按鈕文字",
            value=return_button.get("text", "返回登入")
        )
        
        # 更新配置
        auth_config["privacy_policy"]["title"] = title
        auth_config["privacy_policy"]["last_updated"] = last_updated
        
        # 更新返回按鈕
        if "return_button" not in auth_config["privacy_policy"]:
            auth_config["privacy_policy"]["return_button"] = {}
        
        auth_config["privacy_policy"]["return_button"]["link"] = return_link
        auth_config["privacy_policy"]["return_button"]["text"] = return_text
    # 服務條款設定    
    with tab5:
        st.header("服務條款設定")
        
        service_term_config = auth_config.get("service_term", {})
        
        title = st.text_input(
            "標題",
            value=service_term_config.get("title", "服務條款"),
            key="service_term_title"
        )
        
        last_updated = st.text_input(
            "最後更新日期",
            value=service_term_config.get("last_updated", "最後更新日期：2024年12月4日"),
            key="service_term_last_updated"
        )
        
        # 各區段編輯
        st.subheader("條款區段")
        
        sections = service_term_config.get("sections", {})
        
        # 定義所有區段及其結構
        section_definitions = [
            {
                "key": "acceptance",
                "default_title": "1. 接受條款",
                "has_content": True,
                "has_intro": False,
                "has_list_items": False
            },
            {
                "key": "description",
                "default_title": "2. 服務描述",
                "has_content": True,
                "has_intro": False,
                "has_list_items": False
            },
            {
                "key": "account",
                "default_title": "3. 用戶帳戶",
                "has_content": True,
                "has_intro": False,
                "has_list_items": False
            },
            {
                "key": "subscription",
                "default_title": "4. 訂閱和付款",
                "has_content": True,
                "has_intro": False,
                "has_list_items": False
            },
            {
                "key": "behavior",
                "default_title": "5. 用戶行為",
                "has_content": False,
                "has_intro": True,
                "has_list_items": True
            },
            {
                "key": "intellectual_property",
                "default_title": "6. 知識產權",
                "has_content": True,
                "has_intro": False,
                "has_list_items": False
            },
            {
                "key": "disclaimer",
                "default_title": "7. 免責聲明",
                "has_content": True,
                "has_intro": False,
                "has_list_items": False
            },
            {
                "key": "limitation",
                "default_title": "8. 責任限制",
                "has_content": True,
                "has_intro": False,
                "has_list_items": False
            },
            {
                "key": "modification",
                "default_title": "9. 修改服務",
                "has_content": True,
                "has_intro": False,
                "has_list_items": False
            },
            {
                "key": "contact",
                "default_title": "10. 聯繫我們",
                "has_content": True,
                "has_intro": False,
                "has_list_items": False
            }
        ]
        
        # 動態生成所有區段的編輯界面
        for section_def in section_definitions:
            section_key = section_def["key"]
            section_data = sections.get(section_key, {})
            
            st.markdown(f"#### {section_def['default_title']}")
            
            # 標題
            section_title = st.text_input(
                f"{section_key} 標題",
                value=section_data.get("title", section_def["default_title"]),
                key=f"service_term_{section_key}_title"
            )
            
            # 內容 (如果適用)
            if section_def["has_content"]:
                section_content = st.text_area(
                    f"{section_key} 內容",
                    value=section_data.get("content", ""),
                    key=f"service_term_{section_key}_content"
                )
            
            # 介紹 (如果適用)
            if section_def["has_intro"]:
                section_intro = st.text_area(
                    f"{section_key} 介紹",
                    value=section_data.get("intro", ""),
                    key=f"service_term_{section_key}_intro"
                )
            
            # 列表項目 (如果適用)
            if section_def["has_list_items"]:
                st.markdown(f"##### {section_key} 列表項目")
                
                # 初始化 session_state 來存儲列表項目
                list_items_key = f"service_term_{section_key}_items"
                if list_items_key not in st.session_state:
                    list_items = section_data.get("list_items", [])
                    if not list_items:
                        list_items = [""]
                    st.session_state[list_items_key] = list_items
                
                # 新增列表項目的函數
                def add_list_item(section_key):
                    def _add_item():
                        st.session_state[f"service_term_{section_key}_items"].append("")
                    return _add_item
                
                # 刪除列表項目的函數
                def delete_last_list_item(section_key):
                    def _delete_item():
                        if len(st.session_state[f"service_term_{section_key}_items"]) > 1:
                            st.session_state[f"service_term_{section_key}_items"].pop()
                    return _delete_item
                
                # 顯示現有項目的輸入框
                updated_items = []
                for i, item in enumerate(st.session_state[list_items_key]):
                    item_value = st.text_input(
                        f"{section_key} 項目 #{i+1}",
                        value=item,
                        key=f"service_term_{section_key}_item_{i}"
                    )
                    updated_items.append(item_value)
                
                # 更新 session_state 中的列表項目
                st.session_state[list_items_key] = updated_items
                
                # 新增/刪除項目的按鈕
                col1, col2 = st.columns(2)
                
                with col1:
                    st.button(
                        f"➕ 新增 {section_key} 項目",
                        on_click=add_list_item(section_key),
                        key=f"service_term_add_{section_key}_item"
                    )
                
                with col2:
                    st.button(
                        f"➖ 刪除最後一個 {section_key} 項目",
                        on_click=delete_last_list_item(section_key),
                        disabled=len(st.session_state[list_items_key]) <= 1,
                        key=f"service_term_delete_{section_key}_item"
                    )
            
            # 更新配置
            if "service_term" not in auth_config:
                auth_config["service_term"] = {}
                
            if "sections" not in auth_config["service_term"]:
                auth_config["service_term"]["sections"] = {}
            
            if section_key not in auth_config["service_term"]["sections"]:
                auth_config["service_term"]["sections"][section_key] = {}
            
            auth_config["service_term"]["sections"][section_key]["title"] = section_title
            
            if section_def["has_content"]:
                auth_config["service_term"]["sections"][section_key]["content"] = section_content
            
            if section_def["has_intro"]:
                auth_config["service_term"]["sections"][section_key]["intro"] = section_intro
            
            if section_def["has_list_items"]:
                auth_config["service_term"]["sections"][section_key]["list_items"] = st.session_state[f"service_term_{section_key}_items"]
            
            st.markdown("---")
        
        # 返回按鈕設定
        st.subheader("返回按鈕")
        
        return_button = service_term_config.get("return_button", {})
        return_link = st.text_input(
            "返回連結",
            value=return_button.get("link", "/app"),
            key="service_term_return_link"
        )
        return_text = st.text_input(
            "返回按鈕文字",
            value=return_button.get("text", "返回登入"),
            key="service_term_return_text"
        )
        
        # 更新配置
        auth_config["service_term"]["title"] = title
        auth_config["service_term"]["last_updated"] = last_updated
        
        # 更新返回按鈕
        if "return_button" not in auth_config["service_term"]:
            auth_config["service_term"]["return_button"] = {}
        
        auth_config["service_term"]["return_button"]["link"] = return_link
        auth_config["service_term"]["return_button"]["text"] = return_text

    # 導航欄設定
    with tab6:
        st.header("導航欄設定")
        
        navbar_config = auth_config.get("navbar", {})
        
        # Logo 設定
        st.subheader("Logo 設定")
        
        logo = navbar_config.get("logo", {})
        logo_link = st.text_input(
            "Logo 連結",
            value=logo.get("link", "/")
        )
        logo_image_path = st.text_input(
            "Logo 圖片路徑",
            value=logo.get("image_path", "app/static/logo.png")
        )
        logo_alt_text = st.text_input(
            "Logo 替代文字",
            value=logo.get("alt_text", "三卓科技")
        )
        logo_height = st.text_input(
            "Logo 高度",
            value=logo.get("height", "40")
        )
        
        # 更新配置
        if "navbar" not in auth_config:
            auth_config["navbar"] = {}
        
        if "logo" not in auth_config["navbar"]:
            auth_config["navbar"]["logo"] = {}
        
        auth_config["navbar"]["logo"]["link"] = logo_link
        auth_config["navbar"]["logo"]["image_path"] = logo_image_path
        auth_config["navbar"]["logo"]["alt_text"] = logo_alt_text
        auth_config["navbar"]["logo"]["height"] = logo_height
        
        if "toggle_button" not in auth_config["navbar"]:
            auth_config["navbar"]["toggle_button"] = {}
        
        auth_config["navbar"]["toggle_button"]["title"] = "Navigation Toggle"    

    # 儲存按鈕
    if st.button("儲存變更", type="primary", key="save_auth_config"):
        # 儲存配置    
        save_auth_config(auth_config)    
        st.success("配置已成功儲存！")    

    # 顯示當前配置 (僅在開發模式)
    with st.expander("查看當前配置 (YAML格式)"):
        st.code(yaml.dump(auth_config, allow_unicode=True, sort_keys=False), language="yaml")
