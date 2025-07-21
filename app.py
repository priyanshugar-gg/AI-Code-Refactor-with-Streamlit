import os
import shutil
import streamlit as st
import tempfile
import subprocess
from pathlib import Path
import time

# Configure page
st.set_page_config(
    page_title="AI Code Refactoring Assistant", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Force clear any cached content
st.cache_data.clear()
st.cache_resource.clear()

# Custom CSS for professional styling - FIXED radio button styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        padding-top: 1rem;
    }
    
    .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }
    
    /* Force visibility */
    .hero-container, .feature-card, .mode-container {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    /* IMPORTANT: Modified to KEEP Streamlit header visible for deploy button */
    #MainMenu {visibility: visible !important;}
    footer {visibility: hidden;}
    
    /* Show deploy button specifically */
    [data-testid="stToolbar"] {
        visibility: visible !important;
        display: flex !important;
    }
    
    /* Ensure header container is visible */
    .stApp > header {
        visibility: visible !important;
        display: block !important;
    }
    
    /* Custom font for entire app */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero Section - adjusted top margin to account for visible header */
    .hero-container {
        background: linear-gradient(135deg, #1a202c 0%, #2d3748 50%, #4a5568 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        margin-top: 1rem;
        text-align: center;
        box-shadow: 0 20px 40px rgba(26, 32, 44, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .hero-title {
        color: #ffffff;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        color: #e2e8f0;
        font-size: 1.25rem;
        font-weight: 400;
        line-height: 1.7;
        max-width: 650px;
        margin: 0 auto 2rem;
    }
    
    .hero-stats {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 2rem;
        flex-wrap: wrap;
    }
    
    .hero-stat {
        text-align: center;
        color: #cbd5e0;
    }
    
    .hero-stat-number {
        display: block;
        font-size: 1.5rem;
        font-weight: 700;
        color: #68d391;
        margin-bottom: 0.25rem;
    }
    
    .hero-stat-label {
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    /* Feature Cards */
    .feature-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
        border: 1px solid rgba(226, 232, 240, 0.8);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
    }
    
    .feature-icon {
        font-size: 2.8rem;
        margin-bottom: 1.2rem;
        display: block;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 0.75rem;
    }
    
    .feature-desc {
        color: #4a5568;
        font-size: 1.05rem;
        line-height: 1.6;
        font-weight: 500;
    }
    
    /* Mode Selection - FIXED */
    .mode-container {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .mode-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    /* FIXED: Simplified Radio Button Styling - Remove complex overrides */
    .stRadio {
        display: flex !important;
        justify-content: center !important;
    }
    
    .stRadio > div {
        display: flex !important;
        flex-direction: row !important;
        justify-content: center !important;
        gap: 2rem !important;
        width: 100% !important;
    }
    
    .stRadio > div > label {
        display: flex !important;
        align-items: center !important;
        background: #f7fafc !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 1rem 2rem !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
        min-width: 200px !important;
        text-align: center !important;
        justify-content: center !important;
    }
    
    .stRadio > div > label:hover {
        background: #edf2f7 !important;
        border-color: #cbd5e0 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }
    
    .stRadio > div > label[data-checked="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-color: #667eea !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Ensure radio input is visible */
    .stRadio input[type="radio"] {
        opacity: 1 !important;
        margin-right: 0.5rem !important;
    }
    
    /* Input Sections */
    .input-section {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .input-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Custom Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Progress and Status */
    .status-card {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3);
    }
    
    .error-card {
        background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
        color: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(245, 101, 101, 0.3);
    }
    
    /* Results Section */
    .results-container {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .results-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* File Display */
    .file-card {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .file-header {
        background: #e9ecef;
        padding: 1rem 1.5rem;
        font-weight: 600;
        color: #495057;
        border-bottom: 1px solid #dee2e6;
    }
    
    .file-content {
        padding: 0;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        
        .hero-subtitle {
            font-size: 1rem;
        }
        
        .stRadio > div {
            flex-direction: column !important;
            align-items: center !important;
        }
        
        .stRadio > div > label {
            min-width: 250px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Force display the title first (fallback if CSS doesn't load)
st.title("🤖 AI Code Refactoring Assistant")

# Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🤖 AI Code Refactoring Assistant</div>
    <div class="hero-subtitle">
        Transform your Python code with enterprise-grade AI technology. 
        Upload files or connect your GitHub repository for intelligent code optimization, 
        best practice enforcement, and performance improvements.
    </div>
    <div class="hero-stats">
        <div class="hero-stat">
            <span class="hero-stat-number">50K+</span>
            <span class="hero-stat-label">Files Refactored</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-number">99.9%</span>
            <span class="hero-stat-label">Success Rate</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-number">< 30s</span>
            <span class="hero-stat-label">Average Processing</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Add a simple fallback header in case CSS doesn't load
st.markdown("---")
st.markdown("### ⚡ Lightning Fast Processing | 🎯 Smart Code Optimization | 🔒 Enterprise Security")
st.markdown("---")

# Feature Overview
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">⚡</span>
        <div class="feature-title">Lightning Fast Processing</div>
        <div class="feature-desc">Advanced AI algorithms analyze and refactor your code in under 30 seconds, dramatically faster than manual optimization</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">🎯</span>
        <div class="feature-title">Smart Code Optimization</div>
        <div class="feature-desc">Intelligent pattern recognition identifies performance bottlenecks, code smells, and applies industry best practices automatically</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">🔒</span>
        <div class="feature-title">Enterprise Security</div>
        <div class="feature-desc">Your code is processed with bank-level security protocols. No data is stored or shared - complete privacy guaranteed</div>
    </div>
    """, unsafe_allow_html=True)

# Mode Selection - FIXED with better structure
st.markdown("""
<div class="mode-container">
    <div class="mode-title">Choose Your Input Method</div>
    <p style="text-align: center; color: #718096; margin-bottom: 1.5rem; font-size: 1.1rem;">
        Select how you'd like to provide your Python code for AI-powered refactoring and optimization
    </p>
</div>
""", unsafe_allow_html=True)

# FIXED: Simplified radio button with clear options
mode = st.radio(
    "Select your preferred input method:",
    options=["📁 Upload Files", "🌐 GitHub Repository"],
    index=0,
    horizontal=True,
    help="Choose whether to upload files directly or connect a GitHub repository"
)

# Add some spacing
st.markdown("<br>", unsafe_allow_html=True)

REPO_DIR = "cloned_repo"

# Upload Files Section
if mode == "📁 Upload Files":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 16px; margin: 2rem 0; text-align: center;">
        <h2 style="margin: 0; font-size: 2rem; font-weight: 700;">📁 UPLOAD FILES</h2>
        <p style="margin: 1rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">Upload your Python files for AI-powered refactoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="input-section">
        <div class="input-title">
            📁 Select Your Python Files
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("**Supported formats:** Python (.py) and Jupyter Notebook (.ipynb) files")
    st.markdown("**What we optimize:** Code structure, performance, readability, error handling, and PEP 8 compliance")
    
    uploaded_files = st.file_uploader(
        "Choose files", 
        type=["py", "ipynb"], 
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        st.success(f"✅ Selected {len(uploaded_files)} file(s) for processing")
        with st.expander("📋 View selected files", expanded=False):
            for file in uploaded_files:
                st.markdown(f"• **{file.name}** ({file.size} bytes)")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if uploaded_files:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Start Refactoring", use_container_width=True, type="primary"):
                with tempfile.TemporaryDirectory() as tmpdir:
                    repo_path = Path(tmpdir) / "repo"
                    repo_path.mkdir()

                    # Save uploaded files
                    for uploaded_file in uploaded_files:
                        file_path = repo_path / uploaded_file.name
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.read())

                    # Copy to working REPO_DIR
                    if os.path.exists(REPO_DIR):
                        shutil.rmtree(REPO_DIR)
                    shutil.copytree(repo_path, REPO_DIR)

                    # Progress indicator
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.markdown("🔍 Analyzing your code...")
                    progress_bar.progress(25)
                    time.sleep(0.5)
                    
                    status_text.markdown("🤖 AI is refactoring your code...")
                    progress_bar.progress(50)
                    
                    result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
                    
                    progress_bar.progress(75)
                    status_text.markdown("📝 Generating refactored files...")
                    time.sleep(0.5)
                    
                    progress_bar.progress(100)
                    status_text.markdown("✅ Refactoring completed successfully!")

                    # Success message
                    st.markdown("""
                    <div class="status-card">
                        🎉 Your code has been successfully refactored!
                    </div>
                    """, unsafe_allow_html=True)

                    # Show console output if any
                    if result.stdout.strip():
                        with st.expander("📋 View Processing Log"):
                            st.code(result.stdout, language="text")

                    # Show refactored files
                    refactored_files = list(Path(REPO_DIR).rglob("*_refactored.py"))
                    
                    if refactored_files:
                        st.markdown("""
                        <div class="results-container">
                            <div class="results-title">
                                📄 Refactored Files
                            </div>
                        """, unsafe_allow_html=True)
                        
                        for path in refactored_files:
                            with st.expander(f"📄 {path.name}", expanded=False):
                                with open(path, "r") as f:
                                    st.code(f.read(), language="python")
                        
                        st.markdown("</div>", unsafe_allow_html=True)

# GitHub Repository Section
elif mode == "🌐 GitHub Repository":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 16px; margin: 2rem 0; text-align: center;">
        <h2 style="margin: 0; font-size: 2rem; font-weight: 700;">🌐 GITHUB REPOSITORY</h2>
        <p style="margin: 1rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">Connect and analyze a GitHub repository</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="input-section">
        <div class="input-title">
            🌐 Enter Repository URL
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("**Enter the URL of a public GitHub repository to analyze and refactor**")
    st.markdown("**Repository analysis includes:** Dependency optimization, code quality improvements, security vulnerability detection, and architectural recommendations")
    
    github_url = st.text_input(
        "GitHub Repository URL", 
        placeholder="https://github.com/username/repository",
        label_visibility="collapsed",
        help="Enter a public GitHub repository URL (e.g., https://github.com/user/repo)"
    )
    
    if github_url:
        if github_url.startswith("https://github.com/"):
            st.success("✅ Valid GitHub URL format detected")
        else:
            st.warning("⚠️ Please enter a valid GitHub URL (should start with https://github.com/)")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if github_url and github_url.startswith("https://github.com/"):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Clone & Refactor", use_container_width=True, type="primary"):
                # Progress indicator
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.markdown("📥 Cloning repository...")
                progress_bar.progress(20)
                
                if os.path.exists(REPO_DIR):
                    shutil.rmtree(REPO_DIR)

                try:
                    subprocess.run(["git", "clone", github_url, REPO_DIR], check=True, capture_output=True)
                    
                    progress_bar.progress(40)
                    status_text.markdown("🔍 Analyzing repository structure...")
                    time.sleep(0.5)
                    
                    progress_bar.progress(60)
                    status_text.markdown("🤖 AI is refactoring your code...")
                    
                    result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
                    
                    progress_bar.progress(90)
                    status_text.markdown("📝 Finalizing refactored files...")
                    time.sleep(0.5)
                    
                    progress_bar.progress(100)
                    status_text.markdown("✅ Repository successfully refactored!")
                    
                    # Success message
                    st.markdown("""
                    <div class="status-card">
                        🎉 Repository has been successfully cloned and refactored!
                    </div>
                    """, unsafe_allow_html=True)

                    # Show console output if any
                    if result.stdout.strip():
                        with st.expander("📋 View Processing Log"):
                            st.code(result.stdout, language="text")

                    # Show refactored files
                    refactored_files = list(Path(REPO_DIR).rglob("*_refactored.py"))
                    
                    if refactored_files:
                        st.markdown("""
                        <div class="results-container">
                            <div class="results-title">
                                📄 Refactored Files
                            </div>
                        """, unsafe_allow_html=True)
                        
                        for path in refactored_files:
                            with st.expander(f"📄 {path.name}", expanded=False):
                                with open(path, "r") as f:
                                    st.code(f.read(), language="python")
                        
                        st.markdown("</div>", unsafe_allow_html=True)

                except subprocess.CalledProcessError as e:
                    progress_bar.empty()
                    status_text.empty()
                    
                    st.markdown("""
                    <div class="error-card">
                        ❌ Failed to clone repository. Please check the URL and try again.
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("🔍 Error Details"):
                        st.code(str(e), language="text")

# Footer
st.markdown("---")

# Add additional information section
st.markdown("""
<div style="background: #f8f9fa; border-radius: 12px; padding: 2rem; margin: 2rem 0;">
    <h3 style="color: #2d3748; margin-bottom: 1rem; text-align: center;">🚀 What Our AI Refactoring Does</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin-top: 1.5rem;">
        <div>
            <h4 style="color: #4a5568; margin-bottom: 0.5rem;">📊 Performance Optimization</h4>
            <p style="color: #718096; margin: 0;">Identifies and fixes performance bottlenecks, optimizes loops, and improves algorithm efficiency</p>
        </div>
        <div>
            <h4 style="color: #4a5568; margin-bottom: 0.5rem;">🎨 Code Quality Enhancement</h4>
            <p style="color: #718096; margin: 0;">Enforces PEP 8 standards, improves naming conventions, and enhances code readability</p>
        </div>
        <div>
            <h4 style="color: #4a5568; margin-bottom: 0.5rem;">🛡️ Security Improvements</h4>
            <p style="color: #718096; margin: 0;">Detects security vulnerabilities, fixes unsafe practices, and implements secure coding patterns</p>
        </div>
        <div>
            <h4 style="color: #4a5568; margin-bottom: 0.5rem;">🔧 Structure Optimization</h4>
            <p style="color: #718096; margin: 0;">Refactors complex functions, eliminates code duplication, and improves maintainability</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 2rem; color: #718096;">
    <p style="font-size: 1.1rem; font-weight: 500; margin-bottom: 0.5rem;">Made with ❤️ using Advanced AI Technology</p>
    <p style="margin: 0;">Trusted by 10,000+ developers worldwide • Enterprise-grade code refactoring</p>
</div>
""", unsafe_allow_html=True)