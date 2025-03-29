import streamlit as st
from datetime import datetime
import uuid

def save_to_project(content_type, content, description):
    """
    Save content to the current project
    
    Args:
        content_type (str): Type of content ('text' or 'image')
        content (str): The content to save
        description (str): Description of the content
    
    Returns:
        bool: True if saved successfully, False otherwise
    """
    if not st.session_state.current_project:
        st.error("No active project. Please create or select a project first.")
        return False
    
    project_idx = next((i for i, p in enumerate(st.session_state.projects) 
                        if p["id"] == st.session_state.current_project), None)
    
    if project_idx is None:
        st.error("Project not found.")
        return False
    
    asset_id = str(uuid.uuid4())
    asset = {
        "id": asset_id,
        "type": content_type,
        "content": content,
        "description": description,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    st.session_state.projects[project_idx]["assets"].append(asset)
    
    # Add to history
    history_item = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "project_id": st.session_state.current_project,
        "project_name": st.session_state.projects[project_idx]["name"],
        "asset_id": asset_id,
        "asset_type": content_type,
        "description": description
    }
    st.session_state.history.append(history_item)
    
    return True

def get_all_assets():
    """
    Get all assets from all projects with project information attached
    
    Returns:
        list: List of assets with project information
    """
    all_assets = []
    for project in st.session_state.projects:
        for asset in project["assets"]:
            asset_with_project = asset.copy()
            asset_with_project["project_name"] = project["name"]
            asset_with_project["project_id"] = project["id"]
            all_assets.append(asset_with_project)
    
    return all_assets

def get_project_assets(project_id):
    """
    Get all assets for a specific project
    
    Args:
        project_id (str): ID of the project
    
    Returns:
        list: List of assets for the specified project or empty list if project not found
    """
    project = next((p for p in st.session_state.projects if p["id"] == project_id), None)
    if not project:
        return []
    
    return project["assets"]