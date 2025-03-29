import streamlit as st
import json
import base64
import uuid
from io import BytesIO
from PIL import Image
from datetime import datetime
import time

# Import utility functions
from utils.content_generation.content_generation import generate_text, generate_image
from utils.project_management.project_management import create_project, export_project
from utils.asset_management.asset_management import save_to_project
from utils.session_helpers.session_helpers import initialize_session_state

# Set page configuration
st.set_page_config(
    page_title="CreativeFlow AI Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply CSS
with open("static/styles.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize session state
initialize_session_state()

# Main layout
def main():
    # Custom header with modern design
    st.markdown("""
    <header>
        <h1>🎨 CreativeFlow AI Studio</h1>
        <p>AI-Powered Content Generation Pipeline for Creative Agencies</p>
    </header>
    """, unsafe_allow_html=True)
    
    # Create tabs with modern styling
    tabs = st.tabs(["Dashboard", "Content Generator", "Asset Library", "Projects", "Settings"])
    
    # Dashboard Tab
    with tabs[0]:
        st.header("Dashboard")
        
        # Display quick stats with modern cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="stat-card projects">
                <h3>Projects</h3>
                <p>{len(st.session_state.projects)}</p>
                <small>Total projects</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_assets = sum(len(p["assets"]) for p in st.session_state.projects)
            st.markdown(f"""
            <div class="stat-card assets">
                <h3>Assets</h3>
                <p>{total_assets}</p>
                <small>Total content pieces</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-card activity">
                <h3>Activity</h3>
                <p>{len(st.session_state.history)}</p>
                <small>Recent generations</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Recent projects with animations
        st.markdown("""
        <h2 class="animated">Recent Projects</h2>
        """, unsafe_allow_html=True)
        
        if not st.session_state.projects:
            st.info("No projects yet. Create a new project in the Projects tab.")
        else:
            recent_projects = sorted(st.session_state.projects, 
                                    key=lambda x: x["created_at"], 
                                    reverse=True)[:3]
            
            for i, project in enumerate(recent_projects):
                st.markdown(f"""
                <div class="project-card hover-elevate" style="animation-delay: {i * 0.1}s">
                    <h3>{project['name']} <span style="float: right; font-size: 0.9rem; background: var(--grey-200); padding: 3px 10px; border-radius: 20px;">{len(project['assets'])} assets</span></h3>
                    <p><strong>Created:</strong> {project['created_at']}</p>
                    <p>{project['description'][:150]}{'...' if len(project['description']) > 150 else ''}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Recent activity with modern styling
        st.markdown("""
        <h2 class="animated" style="animation-delay: 0.2s">Recent Activity</h2>
        """, unsafe_allow_html=True)
        
        if not st.session_state.history:
            st.info("No activity recorded yet.")
        else:
            recent_history = sorted(st.session_state.history, 
                                   key=lambda x: x["timestamp"], 
                                   reverse=True)[:5]
            
            for i, item in enumerate(recent_history):
                # Determine icon based on asset type
                icon = "📝" if item['asset_type'] == "text" else "🖼️"
                
                st.markdown(f"""
                <div class="project-card hover-elevate" style="animation-delay: {(i * 0.1) + 0.3}s">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div>
                            <span style="font-size: 1.2rem; margin-right: 10px;">{icon}</span>
                            <strong>{item['asset_type'].capitalize()}</strong> for <strong>{item['project_name']}</strong>
                        </div>
                        <span style="font-size: 0.8rem; color: var(--grey-600);">{item['timestamp']}</span>
                    </div>
                    <p style="margin-top: 10px;">{item['description'][:100]}{'...' if len(item['description']) > 100 else ''}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Content Generator Tab
    with tabs[1]:
        st.header("Content Generator")
        
        # Check for API key with styled alert
        if not st.session_state.api_key:
            st.markdown("""
            <div style="background-color: #fff8e6; border-left: 5px solid #ffc107; padding: 15px; border-radius: 4px; margin-bottom: 20px;">
                <strong style="color: #856404;">⚠️ API Key Required</strong>
                <p style="margin: 5px 0 0 0;">Please set your Together AI API key in the Settings tab before generating content.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Project selection with modern UI
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.session_state.projects:
                project_names = ["None"] + [p["name"] for p in st.session_state.projects]
                selected_project = st.selectbox("Select Project", project_names)
                
                if selected_project != "None":
                    project = next((p for p in st.session_state.projects if p["name"] == selected_project), None)
                    if project:
                        st.session_state.current_project = project["id"]
                    else:
                        st.session_state.current_project = None
                else:
                    st.session_state.current_project = None
            else:
                st.markdown("""
                <div style="background-color: #e7f3fe; border-left: 5px solid #2196f3; padding: 15px; border-radius: 4px; margin-bottom: 20px;">
                    <strong style="color: #0c5460;">ℹ️ No Projects</strong>
                    <p style="margin: 5px 0 0 0;">Create a project in the Projects tab to get started.</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            if st.session_state.current_project:
                project = next((p for p in st.session_state.projects if p["id"] == st.session_state.current_project), None)
                if project:
                    st.markdown("""
                    <div style="background-color: #e8f5e9; border-left: 5px solid #4caf50; padding: 15px; border-radius: 4px;">
                        <p style="margin: 0; font-size: 0.8rem;">Active Project</p>
                        <p style="margin: 5px 0 0 0; font-weight: bold; font-size: 1.1rem;">{}</p>
                    </div>
                    """.format(project['name']), unsafe_allow_html=True)
        
        # Display selected project info with better styling
        if st.session_state.current_project:
            project = next((p for p in st.session_state.projects if p["id"] == st.session_state.current_project), None)
            if project:
                st.markdown(f"""
                <div class="glass-effect" style="padding: 20px; border-radius: var(--border-radius-md); margin: 20px 0;">
                    <h3 style="margin-top: 0;">Project Details</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                        <div>
                            <p style="margin: 0; font-size: 0.9rem; color: var(--grey-600);">Description</p>
                            <p style="margin: 3px 0 0 0;">{project['description']}</p>
                        </div>
                        <div>
                            <p style="margin: 0; font-size: 0.9rem; color: var(--grey-600);">Target Audience</p>
                            <p style="margin: 3px 0 0 0;">{project['target_audience'] if project['target_audience'] else 'Not specified'}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Content generation options with modern styled radio
        st.markdown("""
        <h3 style="margin-top: 30px;">Select Content Type</h3>
        """, unsafe_allow_html=True)
        
        generation_type = st.radio("", 
                                  ["Marketing Copy", "Social Media Post", "Campaign Concept", 
                                   "Brand Storytelling", "Visual Content", "Custom Content"],
                                  label_visibility="collapsed")
        
        # Generation form with styled container
        st.markdown(f"""
        <div style="background: white; border-radius: var(--border-radius-md); padding: 5px 20px 20px; box-shadow: var(--card-shadow); margin-top: 20px;">
            <h3 style="margin-top: 15px;">{generation_type} Generator</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form(key="generation_form"):
            if generation_type == "Marketing Copy":
                col1, col2 = st.columns(2)
                with col1:
                    product_name = st.text_input("Product/Service Name")
                with col2:
                    tone = st.selectbox("Tone", ["Professional", "Casual", "Humorous", "Inspirational", "Urgent"])
                
                key_features = st.text_area("Key Features/Selling Points", height=100)
                copy_length = st.select_slider("Copy Length", options=["Short", "Medium", "Long"])
                
                prompt = f"""Create a compelling marketing copy for {product_name}.
                Key features: {key_features}
                Length: {copy_length}
                Tone: {tone}
                Make it persuasive and focused on benefits. Format it nicely with headlines and sections.
                """
                
            elif generation_type == "Social Media Post":
                col1, col2 = st.columns(2)
                with col1:
                    platform = st.selectbox("Platform", ["Instagram", "Twitter/X", "LinkedIn", "Facebook", "TikTok"])
                with col2:
                    topic = st.text_input("Topic/Announcement")
                
                col3, col4 = st.columns(2)
                with col3:
                    include_hashtags = st.checkbox("Include Hashtags")
                with col4:
                    include_call_to_action = st.checkbox("Include Call-to-Action")
                
                prompt = f"""Create an engaging social media post for {platform} about {topic}.
                {'Include relevant hashtags.' if include_hashtags else ''}
                {'Include a strong call-to-action.' if include_call_to_action else ''}
                Make it attention-grabbing and appropriate for the platform's audience.
                """
                
            elif generation_type == "Campaign Concept":
                col1, col2 = st.columns(2)
                with col1:
                    campaign_objective = st.text_input("Campaign Objective")
                with col2:
                    campaign_duration = st.text_input("Campaign Duration (e.g., '2 weeks', '3 months')")
                
                target_audience = st.text_area("Target Audience Description", height=80)
                key_message = st.text_input("Key Message")
                
                prompt = f"""Develop a creative campaign concept with the following details:
                Objective: {campaign_objective}
                Target Audience: {target_audience}
                Key Message: {key_message}
                Duration: {campaign_duration}
                
                Include the following sections:
                1. Campaign Name/Tagline
                2. Concept Overview
                3. Key Visuals Description
                4. Channel Strategy
                5. Expected Outcomes
                """
                
            elif generation_type == "Brand Storytelling":
                col1, col2 = st.columns(2)
                with col1:
                    brand_name = st.text_input("Brand Name")
                with col2:
                    brand_values = st.text_input("Brand Values")
                
                brand_history = st.text_area("Brand History/Background", height=80)
                target_audience = st.text_area("Target Audience", height=80)
                
                prompt = f"""Craft a compelling brand story for {brand_name} with the following elements:
                Brand History: {brand_history}
                Brand Values: {brand_values}
                Target Audience: {target_audience}
                
                Create a narrative that emotionally connects with the audience, highlights the brand's journey,
                and emphasizes its values and vision for the future. The story should be authentic and memorable.
                """
                
            elif generation_type == "Visual Content":
                col1, col2 = st.columns(2)
                with col1:
                    visual_type = st.selectbox("Visual Type", ["Brand Image", "Product Showcase", "Advertisement", "Social Media Graphic"])
                with col2:
                    style = st.selectbox("Style", ["Realistic", "Illustrated", "Minimalist", "Bold & Colorful", "Elegant & Sophisticated"])
                
                description = st.text_area("Detailed Description", height=80)
                theme = st.text_input("Theme/Mood")
                
                prompt = f"""Create a {style.lower()} {visual_type.lower()} with the following details:
                Description: {description}
                Theme/Mood: {theme}
                
                Make it visually striking and appropriate for commercial use. Ensure it has professional quality
                and would be suitable for a {visual_type.lower()}.
                """
                
            elif generation_type == "Custom Content":
                content_description = st.text_area("Describe what you need in detail", height=120)
                additional_context = st.text_area("Any additional context or requirements", height=80)
                
                prompt = f"""Create content based on the following requirements:
                {content_description}
                
                Additional context:
                {additional_context}
                
                Provide a well-structured, creative and professional output that meets these requirements.
                """
            
            # Add a loading indicator that will be shown when generating
            submit_col1, submit_col2 = st.columns([3, 1])
            with submit_col1:
                submitted = st.form_submit_button("Generate Content", use_container_width=True)
            with submit_col2:
                if st.session_state.api_key:
                    st.markdown('<div class="loading-spinner"></div>', unsafe_allow_html=True)
        
        # Generate content on submit
        if submitted:
            if not st.session_state.api_key:
                st.error("Please add your API key in the Settings tab before generating content.")
            else:
                if generation_type == "Visual Content":
                    # Generate image
                    with st.spinner("Creating your visual content..."):
                        image_data = generate_image(prompt)
                        if image_data:
                            st.session_state.generated_content = {
                                "type": "image",
                                "data": image_data,
                                "prompt": prompt,
                                "generation_type": generation_type
                            }
                else:
                    # Generate text
                    with st.spinner("Generating your content..."):
                        text_content = generate_text(prompt)
                        if text_content:
                            st.session_state.generated_content = {
                                "type": "text",
                                "data": text_content,
                                "prompt": prompt,
                                "generation_type": generation_type
                            }
        
        # Display generated content with improved styling
        if "generated_content" in st.session_state and st.session_state.generated_content:
            st.markdown("<div class='animated' style='margin-top: 40px;'>", unsafe_allow_html=True)
            st.subheader("Generated Content")
            st.markdown("</div>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown('<div class="output-container animated">', unsafe_allow_html=True)
                
                # Display content based on type
                if st.session_state.generated_content["type"] == "text":
                    st.markdown(st.session_state.generated_content["data"])
                elif st.session_state.generated_content["type"] == "image":
                    # Handle both URL and base64 image data
                    if isinstance(st.session_state.generated_content["data"], str):
                        if st.session_state.generated_content["data"].startswith('http'):
                            # If it's a URL
                            st.image(st.session_state.generated_content["data"], use_column_width=True)
                        else:
                            # If it's base64
                            try:
                                image_bytes = base64.b64decode(st.session_state.generated_content["data"])
                                image = Image.open(BytesIO(image_bytes))
                                st.image(image, use_column_width=True)
                            except Exception as e:
                                st.error(f"Error displaying image: {str(e)}")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Save to project option with nicer styling
                if st.session_state.current_project:
                    st.markdown("""
                    <div style="background-color: white; border-radius: var(--border-radius-md); padding: 20px; box-shadow: var(--card-shadow); margin-top: 20px; border-top: 3px solid var(--primary-color);">
                        <h4 style="margin-top: 0;">Save to Project</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    content_description = st.text_input("Add a description for this content")
                    
                    save_col1, save_col2 = st.columns([3, 2])
                    
                    with save_col1:
                        if st.button("Save to Current Project", use_container_width=True):
                            content_type = st.session_state.generated_content["type"]
                            content_data = st.session_state.generated_content["data"]
                            
                            with st.spinner("Saving to project..."):
                                if save_to_project(content_type, content_data, content_description):
                                    st.success("Content saved to project successfully!")
                    
                    with save_col2:
                        if st.button("Generate New Content", type="secondary", use_container_width=True):
                            st.session_state.generated_content = {}
                            st.rerun()
    
    # Asset Library Tab
    with tabs[2]:
        st.header("Asset Library")
        
        # Filter options with modern styling
        st.markdown("""
        <div style="background: white; border-radius: var(--border-radius-md); padding: 20px; box-shadow: var(--card-shadow); margin-bottom: 30px;">
            <h3 style="margin-top: 0;">Filter Assets</h3>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            filter_project = st.selectbox(
                "Filter by Project", 
                ["All Projects"] + [p["name"] for p in st.session_state.projects]
            )
        
        with col2:
            filter_type = st.selectbox(
                "Filter by Type",
                ["All Types", "text", "image"]
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Collect all assets
        all_assets = []
        for project in st.session_state.projects:
            for asset in project["assets"]:
                asset_with_project = asset.copy()
                asset_with_project["project_name"] = project["name"]
                asset_with_project["project_id"] = project["id"]
                all_assets.append(asset_with_project)
        
        # Apply filters
        filtered_assets = all_assets
        if filter_project != "All Projects":
            filtered_assets = [a for a in filtered_assets if a["project_name"] == filter_project]
        
        if filter_type != "All Types":
            filtered_assets = [a for a in filtered_assets if a["type"] == filter_type]
        
        # Display assets with modern styling
        if not filtered_assets:
            st.info("No assets found matching your filters.")
        else:
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin: 30px 0 20px;">
                <h2 style="margin: 0;">Asset Gallery</h2>
                <span style="margin-left: 15px; background: var(--primary-color); color: white; padding: 5px 12px; border-radius: 20px; font-size: 0.9rem;">{len(filtered_assets)} items</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Display as grid for images, list for text
            image_assets = [a for a in filtered_assets if a["type"] == "image"]
            text_assets = [a for a in filtered_assets if a["type"] == "text"]
            
            # Show images in a grid with enhanced styling
            if image_assets:
                st.markdown("""
                <h3 style="margin-bottom: 20px;">
                    <span style="display: inline-block; margin-right: 10px;">🖼️</span> 
                    Images
                </h3>
                """, unsafe_allow_html=True)
                
                # Create a responsive grid for images
                cols = st.columns(3)
                for i, asset in enumerate(image_assets):
                    with cols[i % 3]:
                        st.markdown(f"""
                        <div class="gallery-image-container" style="margin-bottom: 25px; animation: fadeIn 0.5s ease forwards; animation-delay: {i * 0.05}s; opacity: 0;">
                        """, unsafe_allow_html=True)
                        
                        # Display the image
                        if asset["content"].startswith('http'):
                            # If it's a URL
                            st.image(asset["content"], 
                                    caption=asset["description"][:30] + "..." if len(asset["description"]) > 30 else asset["description"], 
                                    use_column_width=True,
                                    clamp=True)
                        else:
                            # If it's base64
                            try:
                                image_bytes = base64.b64decode(asset["content"])
                                image = Image.open(BytesIO(image_bytes))
                                st.image(image, 
                                        caption=asset["description"][:30] + "..." if len(asset["description"]) > 30 else asset["description"], 
                                        use_column_width=True, 
                                        output_format="PNG", 
                                        clamp=True)
                            except Exception as e:
                                st.error(f"Error displaying image: {str(e)}")
                        
                        # Add image details
                        st.markdown(f"""
                        <div style="background: white; padding: 10px 15px; border-radius: 0 0 8px 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.07); margin-top: -20px; position: relative; z-index: 1;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-weight: 500; color: var(--primary-dark);">{asset['project_name']}</span>
                                <span style="font-size: 0.8rem; color: var(--grey-600);">{asset['created_at'].split()[0]}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
            
            # Show text in cards with improved styling
            if text_assets:
                st.markdown("""
                <h3 style="margin: 40px 0 20px;">
                    <span style="display: inline-block; margin-right: 10px;">📝</span> 
                    Text Content
                </h3>
                """, unsafe_allow_html=True)
                
                for i, asset in enumerate(text_assets):
                    with st.expander(f"{asset['description']} ({asset['project_name']})"):
                        st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <span style="font-weight: 500; color: var(--primary-dark);">{asset['project_name']}</span>
                            <span style="font-size: 0.8rem; color: var(--grey-600);">{asset['created_at']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <div style="background: var(--grey-100); padding: 15px; border-radius: var(--border-radius-sm); font-family: 'Georgia', serif; line-height: 1.6;">
                            {asset["content"]}
                        </div>
                        """, unsafe_allow_html=True)
    
    # Projects Tab
    with tabs[3]:
        st.header("Projects")
        
        # Create new project button
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("➕ New Project", use_container_width=True, type="primary"):
                st.session_state.show_new_project = True
        
        # Create new project form
        if st.session_state.get("show_new_project", False):
            st.markdown("""
            <div style="background: white; border-radius: var(--border-radius-md); padding: 20px; box-shadow: var(--card-shadow); margin: 20px 0 30px; border-left: 5px solid var(--primary-color);">
                <h3 style="margin-top: 0;">Create New Project</h3>
            """, unsafe_allow_html=True)
            
            with st.form(key="new_project_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    project_name = st.text_input("Project Name")
                
                with col2:
                    target_audience = st.text_input("Target Audience")
                
                project_description = st.text_area("Project Description", height=100)
                brand_guidelines = st.text_area("Brand Guidelines (Optional)", height=100)
                
                col3, col4 = st.columns([3, 1])
                with col3:
                    create_submitted = st.form_submit_button("Create Project", use_container_width=True)
                with col4:
                    if st.form_submit_button("Cancel", use_container_width=True, type="secondary"):
                        st.session_state.show_new_project = False
                        st.rerun()
                
                if create_submitted and project_name and project_description:
                    project_id = create_project(project_name, project_description, brand_guidelines, target_audience)
                    st.session_state.show_new_project = False
                    st.success(f"Project '{project_name}' created successfully!")
                    time.sleep(1)
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # List existing projects with modern cards
        if not st.session_state.projects:
            st.markdown("""
            <div style="background-color: #f5f5f5; border-radius: var(--border-radius-md); padding: 40px; text-align: center; margin-top: 30px;">
                <img src="https://img.icons8.com/clouds/100/000000/folder-invoices.png" style="width: 80px; height: 80px; margin-bottom: 20px;">
                <h3>No Projects Yet</h3>
                <p>Create your first project to get started with content generation.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Create a grid for projects
            project_cols = [st.columns(3) for _ in range((len(st.session_state.projects) + 2) // 3)]
            flattened_cols = [col for cols in project_cols for col in cols]
            
            for i, project in enumerate(st.session_state.projects):
                with flattened_cols[i]:
                    # Calculate asset counts
                    total_assets = len(project['assets'])
                    image_count = len([a for a in project['assets'] if a['type'] == 'image'])
                    text_count = len([a for a in project['assets'] if a['type'] == 'text'])
                    
                    # Create a custom project card
                    st.markdown(f"""
<div style="background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px;">
    <h3>{project['name']}</h3>
    <p>{project['description'][:120]}{'...' if len(project['description']) > 120 else ''}</p>
    <p>Total Assets: {total_assets} | Images: {image_count} | Texts: {text_count}</p>
    <p><strong>Created:</strong> {project['created_at']}</p>
</div>
""", unsafe_allow_html=True)
                    
                    # Project buttons
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button("View Details", key=f"view_{project['id']}", use_container_width=True):
                            st.session_state.current_project_view = project['id']
                    
                    with btn_col2:
                        if st.button("Make Active", key=f"activate_{project['id']}", use_container_width=True, type="secondary"):
                            st.session_state.current_project = project['id']
                            st.success(f"'{project['name']}' is now the active project")
            
            # Project details view
            if st.session_state.get("current_project_view"):
                project = next((p for p in st.session_state.projects if p["id"] == st.session_state.current_project_view), None)
                if project:
                    st.markdown("<hr style='margin: 40px 0 30px;'>", unsafe_allow_html=True)
                    
                    # Project header with close button
                    col1, col2 = st.columns([5, 1])
                    with col1:
                        st.markdown(f"""
                        <h2 style="margin: 0;">{project['name']} Details</h2>
                        """, unsafe_allow_html=True)
                    with col2:
                        if st.button("Close", use_container_width=True, type="secondary"):
                            st.session_state.current_project_view = None
                            st.rerun()
                    
                    # Project info tabs
                    project_tabs = st.tabs(["Overview", "Assets", "Export"])
                    
                    # Overview tab
                    with project_tabs[0]:
                        st.markdown(f"""
                        <div class="glass-effect" style="padding: 20px; border-radius: var(--border-radius-md); margin: 20px 0;">
                            <h3 style="margin-top: 0;">Project Information</h3>
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr style="border-bottom: 1px solid var(--grey-200);">
                                    <td style="padding: 10px 10px 10px 0; width: 150px; color: var(--grey-700);">Description</td>
                                    <td style="padding: 10px 0;">{project['description']}</td>
                                </tr>
                                <tr style="border-bottom: 1px solid var(--grey-200);">
                                    <td style="padding: 10px 10px 10px 0; color: var(--grey-700);">Target Audience</td>
                                    <td style="padding: 10px 0;">{project['target_audience'] if project['target_audience'] else 'Not specified'}</td>
                                </tr>
                                <tr style="border-bottom: 1px solid var(--grey-200);">
                                    <td style="padding: 10px 10px 10px 0; color: var(--grey-700);">Brand Guidelines</td>
                                    <td style="padding: 10px 0;">{project['brand_guidelines'] if project['brand_guidelines'] else 'Not specified'}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 10px 10px 10px 0; color: var(--grey-700);">Created</td>
                                    <td style="padding: 10px 0;">{project['created_at']}</td>
                                </tr>
                            </table>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Assets tab
                    with project_tabs[1]:
                        if not project['assets']:
                            st.info("No assets yet in this project.")
                        else:
                            # Group by type
                            text_assets = [a for a in project['assets'] if a['type'] == 'text']
                            image_assets = [a for a in project['assets'] if a['type'] == 'image']
                            
                            # Display image assets
                            if image_assets:
                                st.markdown("### Images")
                                image_cols = st.columns(3)
                                for i, asset in enumerate(image_assets):
                                    with image_cols[i % 3]:
                                        try:
                                            if isinstance(asset["content"], str) and asset["content"].startswith('http'):
                                                # If it's a URL
                                                st.image(asset["content"], 
                                                        caption=asset["description"], 
                                                        use_column_width=True)
                                            else:
                                                # If it's base64
                                                image_bytes = base64.b64decode(asset["content"])
                                                image = Image.open(BytesIO(image_bytes))
                                                st.image(image, 
                                                        caption=asset["description"], 
                                                        use_column_width=True)
                                            
                                            st.markdown(f"<small>Created: {asset['created_at']}</small>", unsafe_allow_html=True)
                                        except Exception as e:
                                            st.error(f"Error displaying image: {str(e)}")
                            
                            # Display text assets
                            if text_assets:
                                st.markdown("### Text Content")
                                for i, asset in enumerate(text_assets):
                                    # Use custom styling instead of nested expanders
                                    st.markdown(f"""
                                    <div class="text-asset-card">
                                        <h4>{asset['description']}</h4>
                                        <p><small>Created: {asset['created_at']}</small></p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    # Use a container for text content
                                    st.text_area(
                                        "",
                                        value=asset["content"],
                                        height=150,
                                        disabled=True,
                                        key=f"project_text_asset_{asset['id']}"
                                    )
                                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Export tab
                    with project_tabs[2]:
                        st.markdown("""
                        <div style="background-color: #fff8e6; border-left: 5px solid #ffc107; padding: 15px; border-radius: 4px; margin: 20px 0;">
                            <p style="margin: 0;"><strong>Note:</strong> Exporting will create a JSON file containing all project details and assets.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col1, col2 = st.columns([3, 2])
                        with col1:
                            if st.button("Export Project as JSON", use_container_width=True):
                                project_json = export_project(project['id'])
                                if project_json:
                                    st.download_button(
                                        label="Download Project Data",
                                        data=project_json,
                                        file_name=f"{project['name'].replace(' ', '_')}_export.json",
                                        mime="application/json",
                                        key=f"download_{project['id']}"
                                    )
    
    # Settings Tab
    with tabs[4]:
        st.header("Settings")
        
        # Settings in a card layout
        st.markdown("""
        <div style="background: white; border-radius: var(--border-radius-md); padding: 25px; box-shadow: var(--card-shadow); margin: 20px 0;">
            <h3 style="margin-top: 0;">API Credentials</h3>
        """, unsafe_allow_html=True)
        
        api_key = st.text_input("Together AI API Key", type="password", value=st.session_state.api_key)
        api_col1, api_col2 = st.columns([3, 1])
        
        with api_col1:
            if st.button("Save API Key", use_container_width=True):
                st.session_state.api_key = api_key
                st.success("API Key saved successfully!")
        
        st.markdown("""
        <div style="background-color: #e7f3fe; border-left: 5px solid #2196f3; padding: 15px; border-radius: 4px; margin-top: 20px;">
            <p style="margin: 0;"><strong>Note:</strong> Your API key is stored in the session state and is not persisted.
            You'll need to re-enter it if you reload the application.</p>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Advanced settings
        st.markdown("""
        <div style="background: white; border-radius: var(--border-radius-md); padding: 25px; box-shadow: var(--card-shadow); margin: 30px 0;">
            <h3 style="margin-top: 0;">Model Settings</h3>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            default_text_model = st.selectbox(
                "Default Text Generation Model",
                ["meta-llama/Llama-3.3-70B-Instruct-Turbo", "meta-llama/Llama-3-8b-chat", 
                 "mistralai/Mixtral-8x7B-v0.1", "deepseek-ai/DeepSeek-V3"]
            )
            if st.button("Save Text Model", use_container_width=True):
                st.session_state.default_text_model = default_text_model
                st.success("Default text model updated successfully!")
        
        with col2:
            default_image_model = st.selectbox(
                "Default Image Generation Model",
                ["stabilityai/stable-diffusion-xl-base-1.0", "runwayml/stable-diffusion-v1-5", 
                 "stabilityai/stable-diffusion-2-1"]
            )
            if st.button("Save Image Model", use_container_width=True):
                st.session_state.default_image_model = default_image_model
                st.success("Default image model updated successfully!")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Data management
        st.markdown("""
        <div style="background: white; border-radius: var(--border-radius-md); padding: 25px; box-shadow: var(--card-shadow); margin: 30px 0;">
            <h3 style="margin-top: 0; color: #d32f2f;">Data Management</h3>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #ffebee; border-left: 5px solid #d32f2f; padding: 15px; border-radius: 4px; margin-bottom: 20px;">
            <p style="margin: 0;"><strong>Warning:</strong> Clearing data is irreversible. All projects and generated content will be deleted.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 2])
        with col1:
            if st.button("Clear All Projects and History", type="secondary", use_container_width=True):
                st.session_state.show_clear_confirm = True
        
        # Confirmation dialog
        if st.session_state.get("show_clear_confirm", False):
            st.markdown("""
            <div style="background-color: #ffebee; border-radius: var(--border-radius-md); padding: 20px; margin: 20px 0;">
                <h4 style="margin-top: 0; color: #d32f2f;">Confirm Data Deletion</h4>
                <p>Are you sure you want to delete all projects and history? This action cannot be undone.</p>
            </div>
            """, unsafe_allow_html=True)
            
            confirm = st.checkbox("I understand this will delete all projects and cannot be undone")
            
            confirm_col1, confirm_col2 = st.columns(2)
            with confirm_col1:
                if st.button("Cancel", use_container_width=True, type="secondary"):
                    st.session_state.show_clear_confirm = False
                    st.rerun()
            
            with confirm_col2:
                if st.button("Yes, Delete All Data", use_container_width=True, type="primary"):
                    if confirm:
                        st.session_state.projects = []
                        st.session_state.current_project = None
                        st.session_state.generated_content = {}
                        st.session_state.history = []
                        st.session_state.show_clear_confirm = False
                        st.success("All data has been cleared successfully!")
                    else:
                        st.error("Please check the confirmation box before proceeding.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer with modern styling
    st.markdown("""
    <footer>
        <p>CreativeFlow AI Studio © 2025 | Powered by Together AI</p>
        <p style="font-size: 0.8rem; margin-top: 5px;">A professional content generation pipeline for creative agencies</p>
    </footer>
    """, unsafe_allow_html=True)

# Update session helpers
if __name__ == "__main__":
    # Initialize additional session state variables
    if 'show_new_project' not in st.session_state:
        st.session_state.show_new_project = False
    
    if 'current_project_view' not in st.session_state:
        st.session_state.current_project_view = None
    
    if 'show_clear_confirm' not in st.session_state:
        st.session_state.show_clear_confirm = False
    
    main()