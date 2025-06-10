import streamlit as st
import yaml
import os
from typing import Dict, Any

# Set page title and layout
st.set_page_config(page_title="Website Configuration Editor", layout="wide")

def load_config() -> Dict[str, Any]:
    """Load configuration file"""
    try:
        with open("template/config/landing.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        # If file doesn't exist, return empty dictionary
        return {}

def save_config(config: Dict[str, Any]) -> None:
    """Save configuration file"""
    # Ensure directory exists
    os.makedirs("template/config", exist_ok=True)
    with open("template/config/landing.yaml", "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)

def load_auth_config() -> Dict[str, Any]:
    """Load auth.yaml configuration file"""
    try:
        with open("template/config/auth.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        # If file doesn't exist, return empty dictionary
        return {}

def save_auth_config(config: Dict[str, Any]) -> None:
    """Save auth.yaml configuration file"""
    # Ensure directory exists
    os.makedirs("template/config", exist_ok=True)
    with open("template/config/auth.yaml", "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)


# Load existing configuration
config = load_config()
if not config:
    config = {"landing": {}}

landing_config = config.get("landing", {})

auth_config = load_auth_config()
if not auth_config:
    auth_config = {}




# Title
st.title("Website Configuration Editor")
st.markdown("Modify website content and appearance through this form. Click the 'Save Changes' button at the bottom when finished.")
st.markdown("**Note:** The lite version does not support auth.yaml editing except for footer settings. Skip the auth.yaml section if using the lite version.")

# Use tabs to organize different sections of settings
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Hero Section", "Features", "Demo Experience", "Pricing Plans", "FAQ", "Footer Settings"])

# Hero section settings
with tab1:
    st.header("Hero Section Settings")
    
    hero_config = landing_config.get("hero", {})
    
    # Heading
    hero_heading = st.text_area(
        "Heading Text", 
        value=hero_config.get("heading", "Easily Create Lightweight Software Services<br>Micro SaaS"),
        help="Use <br> for line breaks"
    )
    
    # CTA button text
    hero_cta_text = st.text_input(
        "Button Text",
        value=hero_config.get("cta_button", {}).get("text", "Try Now")
    )
    
    # Video source (optional)
    hero_video_source = st.text_input(
        "Video Source URL",
        value=hero_config.get("video", {}).get("source", "")
    )
    
    # Update configuration
    if "hero" not in landing_config:
        landing_config["hero"] = {}
    
    landing_config["hero"]["section_id"] = "home"  # Fixed value
    landing_config["hero"]["heading"] = hero_heading
    
    if "cta_button" not in landing_config["hero"]:
        landing_config["hero"]["cta_button"] = {}
    
    landing_config["hero"]["cta_button"]["text"] = hero_cta_text
    landing_config["hero"]["cta_button"]["link"] = "/app"  # Fixed value
    landing_config["hero"]["cta_button"]["icon"] = "bi bi-chevron-right"  # Fixed value
    
    if hero_video_source:
        if "video" not in landing_config["hero"]:
            landing_config["hero"]["video"] = {}
        landing_config["hero"]["video"]["source"] = hero_video_source
        landing_config["hero"]["video"]["type"] = "video/mp4"  # Fixed value
# Features section settings
with tab2:
    st.header("Features Section Settings")
    
    feature_config = landing_config.get("feature", {})
    
    # Title and subtitle
    feature_title = st.text_input(
        "Title",
        value=feature_config.get("title", "Service Features")
    )
    
    feature_subtitle = st.text_input(
        "Subtitle",
        value=feature_config.get("subtitle", "Integrated Professional Tools, All-in-One Solution")
    )
    
    # Feature items
    st.subheader("Feature Items")
    
    # Initialize session_state to store feature items
    if "feature_items" not in st.session_state:
        feature_items = feature_config.get("list_item", [])
        
        # Ensure there's at least one item
        if not feature_items:
            feature_items = [{
                "column_width": "4",
                "icon_url": "",
                "icon_alt": "",
                "title": "",
                "description": ""
            }]
        
        st.session_state.feature_items = feature_items
    
    # Function to add a feature item
    def add_feature_item():
        st.session_state.feature_items.append({
            "column_width": "4",
            "icon_url": "",
            "icon_alt": "",
            "title": "",
            "description": ""
        })
    
    # Function to delete a feature item
    def delete_last_feature_item():
        if len(st.session_state.feature_items) > 1:
            st.session_state.feature_items.pop()
    
    # Dynamically generate feature item editing areas
    updated_feature_items = []
    
    for i, item in enumerate(st.session_state.feature_items):
        st.markdown(f"#### Item {i+1}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input(
                f"Title #{i+1}", 
                value=item.get("title", ""),
                key=f"feature_title_{i}"
            )
            icon_url = st.text_input(
                f"Icon URL #{i+1}", 
                value=item.get("icon_url", ""),
                key=f"feature_icon_url_{i}"
            )
            icon_alt = st.text_input(
                f"Icon Alt Text #{i+1}", 
                value=item.get("icon_alt", ""),
                key=f"feature_icon_alt_{i}"
            )
        
        with col2:
            column_width = st.select_slider(
                f"Column Width #{i+1}",
                options=["4", "5", "6", "7", "8"],
                value=item.get("column_width", "4"),
                key=f"feature_column_width_{i}"
            )
            description = st.text_area(
                f"Description #{i+1}", 
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
    
    # Update feature items in session_state
    st.session_state.feature_items = updated_feature_items
    
    # Buttons to add/delete items
    col1, col2 = st.columns(2)
    
    with col1:
        st.button("➕ Add Feature Item", on_click=add_feature_item, key="add_feature_item")
    
    with col2:
        st.button("➖ Delete Last Item", 
                on_click=delete_last_feature_item, 
                disabled=len(st.session_state.feature_items) <= 1,
                key="delete_feature_item")
    
    # Update configuration
    if "feature" not in landing_config:
        landing_config["feature"] = {}
    
    landing_config["feature"]["section_id"] = "feature"  # Fixed value
    landing_config["feature"]["title"] = feature_title
    landing_config["feature"]["subtitle"] = feature_subtitle
    landing_config["feature"]["list_item"] = st.session_state.feature_items
# Demo Experience Settings    
with tab3:
    st.header("Demo Experience Settings")
    
    demo_config = landing_config.get("demo", {})
    
    # Title and main title
    demo_heading = st.text_area(
        "Heading",
        value=demo_config.get("heading", "Streamlit+ AI Powered<br>Quick Generator"),
        help="Use <br> for line breaks"
    )
    
    demo_main_title = st.text_input(
        "Main Title",
        value=demo_config.get("main_title", "Focus on developing your Streamlit app, leave membership management and payment processing to us!")
    )
    
    # Image settings
    demo_image_src = st.text_input(
        "Image Source",
        value=demo_config.get("image", {}).get("src", "app/static/cycles.webp")
    )
    
    # Benefits items
    st.subheader("Benefits")
    
    # Initialize session_state to store benefit items
    if "demo_benefits" not in st.session_state:
        benefits = demo_config.get("benefits", [])
        
        # Ensure there's at least one item
        if not benefits:
            benefits = [{
                "icon_class": "fas fa-robot",
                "title": "",
                "description": ""
            }]
        
        st.session_state.demo_benefits = benefits
    
    # Function to add a benefit item
    def add_benefit():
        st.session_state.demo_benefits.append({
            "icon_class": "fas fa-star",
            "title": "",
            "description": ""
        })
    
    # Function to delete a benefit item
    def delete_last_benefit():
        if len(st.session_state.demo_benefits) > 1:
            st.session_state.demo_benefits.pop()
    
    # Dynamically generate benefit item editing areas
    updated_benefits = []
    
    for i, benefit in enumerate(st.session_state.demo_benefits):
        st.markdown(f"#### Benefit {i+1}")
        
        icon_class = st.text_input(
            f"Icon Class #{i+1}", 
            value=benefit.get("icon_class", "fas fa-robot"),
            help="Use Font Awesome icon classes, e.g., fas fa-robot",
            key=f"benefit_icon_class_{i}"
        )
        
        title = st.text_input(
            f"Title #{i+1}", 
            value=benefit.get("title", ""),
            key=f"benefit_title_{i}"
        )
        description = st.text_area(
            f"Description #{i+1}", 
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
    
    # Update benefit items in session_state
    st.session_state.demo_benefits = updated_benefits
    
    # Buttons to add/delete benefits
    col1, col2 = st.columns(2)
    
    with col1:
        st.button("➕ Add Benefit", on_click=add_benefit, key="add_benefit")
    
    with col2:
        st.button("➖ Delete Last Benefit", 
                on_click=delete_last_benefit, 
                disabled=len(st.session_state.demo_benefits) <= 1,
                key="delete_benefit")
    
    # CTA buttons
    st.subheader("CTA Buttons")
    
    # Initialize session_state to store CTA buttons
    if "cta_buttons" not in st.session_state:
        cta_buttons = demo_config.get("cta_buttons", [])
        
        # Ensure there's at least one button
        if not cta_buttons:
            cta_buttons = [{
                "class": "cta-button white",
                "link": "/app",
                "icon": "bi bi-magic",
                "text": "Try AI Generator"
            }]
        
        st.session_state.cta_buttons = cta_buttons
    
    # Function to add a CTA button
    def add_cta_button():
        st.session_state.cta_buttons.append({
            "class": "cta-button-class",
            "link": "/app",
            "text": "New Button"
        })
    
    # Function to delete a CTA button
    def delete_last_cta_button():
        if len(st.session_state.cta_buttons) > 1:
            st.session_state.cta_buttons.pop()
    
    # Dynamically generate button editing areas
    updated_cta_buttons = []
    
    for i, button in enumerate(st.session_state.cta_buttons):
        st.markdown(f"#### Button {i+1}")
        
        text = st.text_input(
            f"Button Text #{i+1}", 
            value=button.get("text", ""),
            key=f"cta_text_{i}"
        )
        link = st.text_input(
            f"Link #{i+1}", 
            value=button.get("link", "/app"),
            key=f"cta_link_{i}"
        )
        
        # Optional fields
        icon = st.text_input(
            f"Icon (Optional) #{i+1}", 
            value=button.get("icon", ""),
            help="Use Bootstrap Icons classes, e.g., bi bi-magic",
            key=f"cta_icon_{i}"
        )
        
        button_class = st.text_input(
            f"CSS Class #{i+1}", 
            value=button.get("class", "cta-button white"),
            help="CSS class for the button, e.g., cta-button white",
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
    
    # Update CTA buttons in session_state
    st.session_state.cta_buttons = updated_cta_buttons
    
    # Buttons to add/delete CTA buttons
    col1, col2 = st.columns(2)
    
    with col1:
        st.button("➕ Add Button", on_click=add_cta_button, key="add_cta_button")
    
    with col2:
        st.button("➖ Delete Last Button", 
                on_click=delete_last_cta_button, 
                disabled=len(st.session_state.cta_buttons) <= 1,
                key="delete_cta_button")
    
    # Update configuration
    if "demo" not in landing_config:
        landing_config["demo"] = {}
    
    landing_config["demo"]["section_id"] = "demo"  # Fixed value
    landing_config["demo"]["heading"] = demo_heading
    landing_config["demo"]["main_title"] = demo_main_title
    
    if "image" not in landing_config["demo"]:
        landing_config["demo"]["image"] = {}
    
    landing_config["demo"]["image"]["src"] = demo_image_src
    landing_config["demo"]["image"]["height"] = "1028"  # Fixed value
    landing_config["demo"]["image"]["width"] = "2168"  # Fixed value
    
    landing_config["demo"]["benefits"] = st.session_state.demo_benefits
    landing_config["demo"]["cta_buttons"] = st.session_state.cta_buttons
# Pricing Plans Settings
with tab4:
    st.header("Pricing Plans Settings")
    
    pricing_config = landing_config.get("pricing", {})
    
    # Title
    pricing_title = st.text_input(
        "Title",
        value=pricing_config.get("title", "Choose Your Plan")
    )
    
    # Plan items
    st.subheader("Plan Items")
    
    # Initialize session_state to store plans
    if "pricing_plans" not in st.session_state:
        plans = pricing_config.get("plans", [])
        
        # Ensure there's at least one plan
        if not plans:
            plans = [{
                "name": "Free Plan",
                "is_popular": False,
                "price": "$0",
                "price_period": "/month",
                "ai_quota": "1 AI generation per month",
                "features": ["Basic layout templates", "Social sharing features", "Basic code optimization"],
                "button": {
                    "link": "https://www.patreon.com/c/3droid/membership",
                    "class": "btn btn-outline w-100",
                    "text": "Get Started"
                }
            }]
        
        st.session_state.pricing_plans = plans
    
    # Function to add a pricing plan
    def add_pricing_plan():
        st.session_state.pricing_plans.append({
            "name": "New Plan",
            "is_popular": False,
            "price": "$0",
            "price_period": "/month",
            "ai_quota": "AI generation quota per month",
            "features": ["Feature 1", "Feature 2"],
            "button": {
                "link": "#",
                "class": "btn btn-outline w-100",
                "text": "Select Plan"
            }
        })
    
    # Function to delete a pricing plan
    def delete_last_pricing_plan():
        if len(st.session_state.pricing_plans) > 1:
            st.session_state.pricing_plans.pop()
    
    # Dynamically generate plan editing areas
    updated_plans = []
    
    for i, plan in enumerate(st.session_state.pricing_plans):
        st.markdown(f"#### Plan {i+1}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                f"Plan Name #{i+1}", 
                value=plan.get("name", ""),
                key=f"plan_name_{i}"
            )
            price = st.text_input(
                f"Price #{i+1}", 
                value=plan.get("price", "$0"),
                key=f"plan_price_{i}"
            )
            price_period = st.text_input(
                f"Price Period #{i+1}", 
                value=plan.get("price_period", "/month"),
                key=f"plan_price_period_{i}"
            )
            ai_quota = st.text_input(
                f"AI Quota #{i+1}", 
                value=plan.get("ai_quota", "1 AI generation per month"),
                key=f"plan_ai_quota_{i}"
            )
        
        with col2:
            is_popular = st.checkbox(
                f"Is Popular Plan #{i+1}", 
                value=plan.get("is_popular", False),
                key=f"plan_is_popular_{i}"
            )
            
            popular_badge_text = ""
            if is_popular:
                popular_badge_text = st.text_input(
                    f"Popular Badge Text #{i+1}", 
                    value=plan.get("popular_badge_text", "Most Popular"),
                    key=f"plan_popular_badge_text_{i}"
                )
        
        # Features list
        st.markdown(f"##### Features List #{i+1}")
        
        # Initialize features list session_state for this plan
        plan_features_key = f"plan_{i}_features"
        if plan_features_key not in st.session_state:
            features = plan.get("features", [])
            
            # Ensure there's at least one feature
            if not features:
                features = [""]
            
            st.session_state[plan_features_key] = features
        
        # Function to add a feature to a plan
        def add_feature_to_plan(plan_idx):
            return lambda: st.session_state[f"plan_{plan_idx}_features"].append("")
        
        # Function to delete a feature from a plan
        def delete_last_feature_from_plan(plan_idx):
            return lambda: st.session_state[f"plan_{plan_idx}_features"].pop() if len(st.session_state[f"plan_{plan_idx}_features"]) > 1 else None
        
        # Dynamically generate features list editing areas
        updated_features = []
        
        for j, feature in enumerate(st.session_state[plan_features_key]):
            feature_text = st.text_input(
                f"Feature #{i+1}-{j+1}", 
                value=feature,
                key=f"plan_{i}_feature_{j}"
            )
            updated_features.append(feature_text)
        
        # Update features list in session_state
        st.session_state[plan_features_key] = updated_features
        
        # Buttons to add/delete features
        col1, col2 = st.columns(2)
        
        with col1:
            st.button(
                f"➕ Add Feature #{i+1}", 
                on_click=add_feature_to_plan(i),
                key=f"add_feature_to_plan_{i}"
            )
        
        with col2:
            st.button(
                f"➖ Delete Last Feature #{i+1}", 
                on_click=delete_last_feature_from_plan(i),
                disabled=len(st.session_state[plan_features_key]) <= 1,
                key=f"delete_feature_from_plan_{i}"
            )
        
        # Button settings
        st.markdown(f"##### Button Settings #{i+1}")
        
        button = plan.get("button", {})
        button_text = st.text_input(
            f"Button Text #{i+1}", 
            value=button.get("text", "Get Started"),
            key=f"plan_button_text_{i}"
        )
        button_link = st.text_input(
            f"Button Link #{i+1}", 
            value=button.get("link", ""),
            key=f"plan_button_link_{i}"
        )
        button_class = st.text_input(
            f"Button CSS Class #{i+1}", 
            value=button.get("class", "btn btn-outline w-100"),
            help="CSS class for the button, e.g., btn btn-outline w-100",
            key=f"plan_button_class_{i}"
        )
        
        # Build plan data
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
    
    # Update plans in session_state
    st.session_state.pricing_plans = updated_plans
    
    # Buttons to add/delete plans
    col1, col2 = st.columns(2)
    
    with col1:
        st.button("➕ Add Plan", on_click=add_pricing_plan, key="add_pricing_plan")
    
    with col2:
        st.button("➖ Delete Last Plan", 
                on_click=delete_last_pricing_plan, 
                disabled=len(st.session_state.pricing_plans) <= 1,
                key="delete_pricing_plan")
    
    # Update configuration
    if "pricing" not in landing_config:
        landing_config["pricing"] = {}
    
    landing_config["pricing"]["section_id"] = "pricing"  # Fixed value
    landing_config["pricing"]["title"] = pricing_title
    landing_config["pricing"]["feature_icon"] = "fas fa-check"  # Fixed value
    landing_config["pricing"]["plans"] = st.session_state.pricing_plans
# FAQ Settings
with tab5:
    st.header("FAQ Settings")
    
    faq_config = landing_config.get("faq", {})
    
    # Title
    faq_title = st.text_input(
        "Title",
        value=faq_config.get("title", "Frequently Asked Questions")
    )
    
    # FAQ Items
    st.subheader("FAQ Items")
    
    # Initialize session_state to store FAQ items
    if "faq_items" not in st.session_state:
        faq_items = faq_config.get("faq_items", [])
        
        # Ensure there's at least one FAQ item
        if not faq_items:
            faq_items = [{
                "question": "Question?",
                "answer": "Answer..."
            }]
        
        st.session_state.faq_items = faq_items
    
    # Function to add an FAQ item
    def add_faq_item():
        st.session_state.faq_items.append({
            "question": "",
            "answer": ""
        })
    
    # Function to delete an FAQ item
    def delete_last_faq_item():
        if len(st.session_state.faq_items) > 1:
            st.session_state.faq_items.pop()
    
    # Dynamically generate FAQ item editing areas
    updated_faq_items = []
    
    for i, item in enumerate(st.session_state.faq_items):
        st.markdown(f"#### Q&A {i+1}")
        
        question = st.text_input(
            f"Question #{i+1}", 
            value=item.get("question", ""),
            key=f"faq_question_{i}"
        )
        answer = st.text_area(
            f"Answer #{i+1}", 
            value=item.get("answer", ""),
            key=f"faq_answer_{i}"
        )
        
        updated_faq_items.append({
            "question": question,
            "answer": answer
        })
        
        if i < len(st.session_state.faq_items) - 1:
            st.markdown("---")
    
    # Update FAQ items in session_state
    st.session_state.faq_items = updated_faq_items
    
    # Buttons to add/delete FAQ items
    col1, col2 = st.columns(2)
    
    with col1:
        st.button("➕ Add FAQ Item", on_click=add_faq_item)
    
    with col2:
        st.button("➖ Delete Last FAQ Item", on_click=delete_last_faq_item, 
                disabled=len(st.session_state.faq_items) <= 1)
    
    # Update configuration
    if "faq" not in landing_config:
        landing_config["faq"] = {}
    
    landing_config["faq"]["title"] = faq_title
    landing_config["faq"]["faq_items"] = st.session_state.faq_items

# Footer settings
with tab6:
    st.header("Footer Settings")
    
    footer_config = auth_config.get("footer", {})
    
    # Logo settings
    st.subheader("Logo Settings")
    logo_src = st.text_input(
        "Logo Image Source",
        value=footer_config.get("logo", {}).get("src", "")
    )
    logo_alt = st.text_input(
        "Logo Alt Text",
        value=footer_config.get("logo", {}).get("alt", "3Droid Financial Technology")
    )
    
    # Social links
    st.subheader("Social Links")
    
    # Initialize session_state to store social links
    if "social_links" not in st.session_state:
        social_links = footer_config.get("social_links", [])
        if not social_links:
            social_links = []
        
        st.session_state.social_links = social_links
    
    # Function to add a social link
    def add_social_link():
        st.session_state.social_links.append({
            "name": "",
            "url": "",
            "icon": ""
        })
    
    # Function to delete a social link
    def delete_last_social_link():
        if len(st.session_state.social_links) > 0:
            st.session_state.social_links.pop()
    
    # Dynamically generate social link editing areas
    updated_social_links = []
    
    for i, link in enumerate(st.session_state.social_links):
        st.markdown(f"#### Link {i+1}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                f"Platform Name #{i+1}", 
                value=link.get("name", ""),
                key=f"social_name_{i}"
            )
            icon = st.text_input(
                f"Icon Code #{i+1}", 
                value=link.get("icon", ""),
                key=f"social_icon_{i}"
            )
        
        with col2:
            url = st.text_input(
                f"Link URL #{i+1}", 
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
    
    # Update social links in session_state
    st.session_state.social_links = updated_social_links
    
    # Buttons to add/delete social links
    col1, col2 = st.columns(2)
    
    with col1:
        st.button(
            "➕ Add Social Link", 
            on_click=add_social_link,
            key="add_social_link"
        )
    
    with col2:
        st.button(
            "➖ Delete Last Social Link", 
            on_click=delete_last_social_link,
            disabled=len(st.session_state.social_links) <= 0,
            key="delete_social_link"
        )
    
    # Update configuration
    if "footer" not in auth_config:
        auth_config["footer"] = {}
    
    if "logo" not in auth_config["footer"]:
        auth_config["footer"]["logo"] = {}
    
    auth_config["footer"]["logo"]["src"] = logo_src
    auth_config["footer"]["logo"]["alt"] = logo_alt
    auth_config["footer"]["social_links"] = st.session_state.social_links

# Save button
if st.button("Save Changes", type="primary"):
    config["landing"] = landing_config
    save_config(config)
    save_auth_config(auth_config)    
    st.success("Configuration saved successfully!")        

# Display current configuration (development mode only)
with st.expander("View Current Configuration (YAML format)"):
    st.code(yaml.dump(config, allow_unicode=True, sort_keys=False), language="yaml")
    st.code(yaml.dump(auth_config, allow_unicode=True, sort_keys=False), language="yaml")

