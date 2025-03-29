# CreativeFlow AI Studio

<div align="center">
  <img src="https://i.imgur.com/oD5cco0.png" alt="CreativeFlow Logo" height="100"/>
  <p><em>Supercharge your creative workflow with AI-powered content generation and management</em></p>
</div>

## 🚀 Overview
CreativeFlow AI Studio is an all-in-one content creation platform that leverages artificial intelligence to streamline the creative process. From ideation to execution, it helps marketers, designers, and content creators generate high-quality assets, organize projects, and maintain brand consistency across campaigns.

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="https://img.shields.io/badge/Content-%F0%9F%93%9D-blue" width="60" alt="Content"/></td>
      <td align="center"><img src="https://img.shields.io/badge/AI-%F0%9F%A7%A0-purple" width="60" alt="AI"/></td>
      <td align="center"><img src="https://img.shields.io/badge/Workflow-%F0%9F%94%84-green" width="60" alt="Workflow"/></td>
    </tr>
    <tr>
      <td align="center"><b>Asset Creation</b></td>
      <td align="center"><b>AI Generation</b></td>
      <td align="center"><b>Project Management</b></td>
    </tr>
  </table>
</div>

## ✨ Features

### 🎨 Creative Asset Generation
- **AI-powered Text Creation** for marketing copy, social posts, and product descriptions
- **Image Generation** using advanced AI models with customizable styles and parameters
- **Content Variations** to explore different creative approaches quickly

### 📂 Project Organization
<div align="center">
  <table>
    <tr>
      <td align="center" width="33%">
        <h3>Projects</h3>
        <img src="https://raw.githubusercontent.com/microsoft/fluentui-system-icons/master/assets/Folder/SVG/ic_fluent_folder_24_regular.svg" width="40"/>
        <p>Organize assets by campaign, client, or initiative</p>
      </td>
      <td align="center" width="33%">
        <h3>Library</h3>
        <img src="https://raw.githubusercontent.com/microsoft/fluentui-system-icons/master/assets/Library/SVG/ic_fluent_library_24_regular.svg" width="40"/>
        <p>Centralized repository for all assets with search and filters</p>
      </td>
      <td align="center" width="33%">
        <h3>Templates</h3>
        <img src="https://raw.githubusercontent.com/microsoft/fluentui-system-icons/master/assets/Document/SVG/ic_fluent_document_24_regular.svg" width="40"/>
        <p>Save and reuse successful creative formats</p>
      </td>
    </tr>
  </table>
</div>

### 🔧 Customizable Workflow
- **Brand Guidelines Integration** to ensure consistent messaging and style
- **Target Audience Profiles** to tailor content to specific segments
- **Asset Modification Tools** for quick adjustments without starting over

### 📊 Analytics and Insights
- Track asset creation metrics and AI usage
- Evaluate content performance
- Identify successful creative patterns

### 🤝 Collaboration Features
- Real-time collaboration on projects
- Version history and tracking
- Export options for various platforms and formats

## 🗂️ Project Structure

```
📦 creative_pipeline/
 ┣ 📜 app.py                  # Main Streamlit application
 ┣ 📜 styles.css              # Custom styling
 ┣ 📂 static/                 # Static assets
 ┣ 📂 modules/                # Core functionality modules
 ┃ ┣ 📜 __init__.py           # Package initialization
 ┃ ┣ 📜 text_generation.py    # AI text generation functionality
 ┃ ┣ 📜 image_generation.py   # AI image generation engine
 ┃ ┣ 📜 project_manager.py    # Project and asset management
 ┃ ┣ 📜 database.py           # Database connections and operations
 ┃ ┗ 📜 utils.py              # Utility functions
 ┣ 📂 data/                   # Local data storage
 ┃ ┣ 📂 projects/             # Project data
 ┃ ┣ 📂 assets/               # Generated assets
 ┃ ┗ 📂 templates/            # Content templates
 ┗ 📜 requirements.txt        # Dependencies
```

## 🛠️ Installation and Setup

### Prerequisites
- Python 3.8+
- Git (optional)

### Quick Start Guide

<details>
<summary><b>1. Clone the Repository</b></summary>

```bash
git clone https://github.com/fouadmahmoud281/creativeflow-ai-studio.git
cd creativeflow-ai-studio
```
</details>

<details>
<summary><b>2. Create a Virtual Environment (Recommended)</b></summary>

```bash
# Using venv
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```
</details>

<details>
<summary><b>3. Install Dependencies</b></summary>

```bash
pip install -r requirements.txt
```
</details>

<details>
<summary><b>4. Set Up API Keys</b></summary>

Create a `.env` file in the root directory with your API keys:

```
OPENAI_API_KEY=your_openai_api_key
STABILITY_API_KEY=your_stability_api_key
# Add other API keys as needed
```
</details>

<details>
<summary><b>5. Launch the Application</b></summary>

```bash
streamlit run app.py
```
</details>

## 🖥️ User Interface

<div align="center">
  <img src="https://raw.githubusercontent.com/microsoft/fluentui-system-icons/master/assets/Window%20Dev%20Tools/SVG/ic_fluent_window_dev_tools_24_regular.svg" alt="Application Screenshot" width="60"/>
</div>

### 🎛️ Navigation and Dashboard

The application features an intuitive interface:

1. **Dashboard**
   - Quick access to recent projects and assets
   - Creation statistics and activity feed
   - Quick-start templates

2. **Projects Hub**
   - Create and manage projects
   - Organize assets by campaign or theme
   - Track project progress and deadlines

3. **Asset Library**
   - Browse all created assets
   - Filter by type, project, date, or tags
   - Preview and edit existing content

4. **Creation Studios**
   - Text Studio for copywriting and content generation
   - Image Studio for visual asset creation
   - Template Studio for saving and applying consistent formats

### 🧰 Content Creation Workflow

1. **Project Setup**
   - Define project parameters and goals
   - Set target audience and brand guidelines
   - Import reference materials

2. **Content Generation**
   - Choose content type (text, image)
   - Specify parameters and style preferences
   - Generate multiple variations with AI assistance

3. **Review and Refine**
   - Compare generated options
   - Make adjustments and regenerate as needed
   - Save finalized assets to the project library

4. **Export and Share**
   - Download in various formats
   - Copy directly to clipboard
   - Share via integrated tools

## 🔍 How It Works

<div align="center">
  <table>
    <tr>
      <td align="center" width="25%"><b>Step 1</b><br>Project Definition</td>
      <td align="center" width="25%"><b>Step 2</b><br>AI Generation</td>
      <td align="center" width="25%"><b>Step 3</b><br>Content Refinement</td>
      <td align="center" width="25%"><b>Step 4</b><br>Asset Management</td>
    </tr>
    <tr>
      <td><img src="https://raw.githubusercontent.com/microsoft/fluentui-system-icons/master/assets/Lightbulb/SVG/ic_fluent_lightbulb_24_regular.svg" width="40"/></td>
      <td><img src="https://raw.githubusercontent.com/microsoft/fluentui-system-icons/master/assets/Brain%20Circuit/SVG/ic_fluent_brain_circuit_24_regular.svg" width="40"/></td>
      <td><img src="https://raw.githubusercontent.com/microsoft/fluentui-system-icons/master/assets/Edit/SVG/ic_fluent_edit_24_regular.svg" width="40"/></td>
      <td><img src="https://raw.githubusercontent.com/microsoft/fluentui-system-icons/master/assets/Save/SVG/ic_fluent_save_24_regular.svg" width="40"/></td>
    </tr>
    <tr>
      <td>Set up project parameters and creative goals</td>
      <td>Leverage AI models to generate content options</td>
      <td>Modify and perfect the generated content</td>
      <td>Organize assets and maintain project library</td>
    </tr>
  </table>
</div>

## 📋 Technical Implementation

### AI Integration

CreativeFlow AI Studio integrates with multiple AI platforms to provide comprehensive content generation:

```python
# Example text generation implementation
def generate_text_content(prompt, parameters):
    """
    Generate text content using AI based on the provided prompt and parameters.
    
    Args:
        prompt (str): The creative brief or content instruction
        parameters (dict): Configuration parameters for the generation
        
    Returns:
        list: Generated text variations
    """
    # Set up the API request based on selected model
    if parameters['model'] == 'gpt':
        response = openai_client.completions.create(
            model=parameters['model_version'],
            prompt=prompt,
            max_tokens=parameters['max_length'],
            temperature=parameters['creativity'],
            n=parameters['num_variations']
        )
        return [choice.text for choice in response.choices]
    
    # Support for additional models can be added here
    
    return []
```

### Project Management System

The application includes a robust project management system:

```python
# Project creation functionality
def create_project(name, description, brand_guidelines="", target_audience=""):
    """
    Create a new creative project with the specified parameters.
    
    Args:
        name (str): Project name
        description (str): Project description
        brand_guidelines (str): Brand guidelines to follow
        target_audience (str): Target audience description
        
    Returns:
        str: ID of the created project
    """
    project_id = str(uuid.uuid4())
    
    # Create project structure
    project = {
        "id": project_id,
        "name": name,
        "description": description,
        "brand_guidelines": brand_guidelines,
        "target_audience": target_audience,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "assets": []
    }
    
    # Save project to database
    save_project(project)
    
    return project_id
```

## 📦 Dependencies

- **streamlit**: Interactive web interface
- **openai**: GPT integration for text generation
- **pillow**: Image processing and manipulation
- **pandas**: Data management and organization
- **SQLite/SQLAlchemy**: Local database management
- **python-dotenv**: Environment variable management

## ⚠️ Disclaimer

<div align="center">
  <img src="https://raw.githubusercontent.com/microsoft/fluentui-system-icons/master/assets/Warning/SVG/ic_fluent_warning_24_regular.svg" width="60" alt="Warning"/>
</div>

CreativeFlow AI Studio is a creative assistance tool. Content created with AI should be reviewed for accuracy, appropriateness, and compliance with applicable laws and regulations. Users are responsible for ensuring that generated content:

1. Does not infringe on intellectual property rights
2. Complies with their company's brand guidelines and policies
3. Adheres to advertising standards and regulations
4. Is verified for factual accuracy

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add some amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="https://raw.githubusercontent.com/microsoft/fluentui-system-icons/master/assets/Mail/SVG/ic_fluent_mail_24_regular.svg" width="30" alt="Email"/></td>
      <td align="center"><img src="https://raw.githubusercontent.com/microsoft/fluentui-system-icons/master/assets/Globe/SVG/ic_fluent_globe_24_regular.svg" width="30" alt="Website"/></td>
      <td align="center"><img src="https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/github.svg" width="30" alt="GitHub"/></td>
    </tr>
    <tr>
      <td align="center"><a href="mailto:fouadmahmoud281@gmail.com">Email</a></td>
      <td align="center"><a href="https://github.com/fouadmahmoud281">Personal Website</a></td>
      <td align="center"><a href="https://github.com/fouadmahmoud281">GitHub</a></td>
    </tr>
  </table>
</div>

## 🔮 Future Development

- **Enhanced AI Models**: Integration with more specialized content generation AI
- **Collaboration Features**: Real-time multi-user editing and commenting
- **Analytics Dashboard**: Advanced insights into content performance
- **Mobile App**: On-the-go content creation and project management
- **API Integration**: Connect with popular marketing platforms and content management systems

---

<div align="center">
  <p><b>Ready to revolutionize your creative workflow?</b></p>
  <p>⭐ Star this repo if you found it useful! ⭐</p>
  <img src="https://raw.githubusercontent.com/microsoft/fluentui-system-icons/master/assets/Star/SVG/ic_fluent_star_24_regular.svg" width="30"/>
</div>
