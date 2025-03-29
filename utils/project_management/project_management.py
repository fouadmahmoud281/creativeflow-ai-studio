import streamlit as st
import uuid
import json
from datetime import datetime

def create_project(name, description, brand_guidelines, target_audience):
    """
    Create a new project and add it to the session state
    
    Args:
        name (str): Project name
        description (str): Project description
        brand_guidelines (str): Brand guidelines
        target_audience (str): Target audience description
    
    Returns:
        str: Project ID
    """
    project_id = str(uuid.uuid4())
    project = {
        "id": project_id,
        "name": name,
        "description": description,
        "brand_guidelines": brand_guidelines,
        "target_audience": target_audience,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "assets": []
    }
    st.session_state.projects.append(project)
    st.session_state.current_project = project_id
    return project_id

def export_project(project_id):
    """
    Export a project as JSON
    
    Args:
        project_id (str): ID of the project to export
    
    Returns:
        str: JSON string representation of the project or None if project not found
    """
    project = next((p for p in st.session_state.projects if p["id"] == project_id), None)
    if not project:
        return None
    
    return json.dumps(project, indent=2)

def get_project_by_id(project_id):
    """
    Get a project by its ID
    
    Args:
        project_id (str): ID of the project to retrieve
    
    Returns:
        dict: Project data or None if not found
    """
    return next((p for p in st.session_state.projects if p["id"] == project_id), None)

def get_project_by_name(project_name):
    """
    Get a project by its name
    
    Args:
        project_name (str): Name of the project to retrieve
    
    Returns:
        dict: Project data or None if not found
    """
    return next((p for p in st.session_state.projects if p["name"] == project_name), None)