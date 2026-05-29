"""
Phase 1 PDF Generator
Generates comprehensive Phase 1 Requirements and File Structure document
Author: Offline Speech Recognition System
Date: May 30, 2026
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from datetime import datetime
import os


def create_phase1_pdf():
    """Generate Phase 1 Requirements PDF"""
    
    # Create PDF
    filename = "PHASE1_REQUIREMENTS_AND_FILE_STRUCTURE.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            rightMargin=0.5*inch, leftMargin=0.5*inch,
                            topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    # Container for PDF elements
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#003366'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#003366'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#003366'),
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#333333'),
        spaceAfter=6,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=6
    )
    
    # ==================== TITLE PAGE ====================
    elements.append(Spacer(1, 0.5*inch))
    
    elements.append(Paragraph("PHASE 1 DEVELOPMENT", title_style))
    elements.append(Paragraph("Offline Speech Recognition System", subtitle_style))
    
    elements.append(Spacer(1, 0.3*inch))
    
    elements.append(Paragraph("Requirements & File Structure Documentation", 
                             ParagraphStyle('subtitle2', parent=styles['Normal'], 
                                          fontSize=12, alignment=TA_CENTER, textColor=colors.HexColor('#666666'))))
    
    elements.append(Spacer(1, 0.5*inch))
    
    # Document info
    doc_info = [
        f"<b>Document Date:</b> May 30, 2026",
        f"<b>Project Type:</b> Offline Speech-to-Text Pipeline",
        f"<b>Technology Stack:</b> Python, OpenAI Whisper, FastAPI",
        f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}"
    ]
    
    for info in doc_info:
        elements.append(Paragraph(info, ParagraphStyle('info', parent=styles['Normal'], 
                                                       fontSize=10, alignment=TA_CENTER)))
        elements.append(Spacer(1, 0.15*inch))
    
    elements.append(PageBreak())
    
    # ==================== TABLE OF CONTENTS ====================
    elements.append(Paragraph("TABLE OF CONTENTS", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    toc_items = [
        "1. Project Overview & Objectives",
        "2. Phase 1 Requirements Summary",
        "3. System Architecture",
        "4. Hardware Requirements",
        "5. Software Requirements",
        "6. Dependencies & Libraries",
        "7. File Structure & Code Requirements",
        "8. Installation Procedure",
        "9. Configuration Setup",
        "10. Testing Procedure",
        "11. Deployment Checklist",
        "12. Next Steps & Phase 2 Roadmap"
    ]
    
    for item in toc_items:
        elements.append(Paragraph(item, normal_style))
        elements.append(Spacer(1, 0.1*inch))
    
    elements.append(PageBreak())
    
    # ==================== SECTION 1: PROJECT OVERVIEW ====================
    elements.append(Paragraph("1. PROJECT OVERVIEW & OBJECTIVES", heading_style))
    elements.append(Spacer(1, 0.15*inch))
    
    overview_text = """
    This project aims to build a <b>complete offline speech recognition system</b> that operates independently 
    without requiring internet connectivity. Phase 1 focuses on establishing the foundation with 
    <b>speech-to-text transcription capabilities</b> using OpenAI's Whisper model deployed locally.
    """
    elements.append(Paragraph(overview_text, normal_style))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("Phase 1 Core Objectives:", subheading_style))
    objectives = [
        "✓ Implement a fully functional, offline speech-to-text system",
        "✓ Convert audio files to text with high accuracy (>95%)",
        "✓ Set up REST API endpoints for programmatic access",
        "✓ Implement model caching and efficient management",
        "✓ Prepare robust foundation for Phase 2 expansion",
        "✓ Ensure system operates completely offline after setup"
    ]
    
    for obj in objectives:
        elements.append(Paragraph(obj, normal_style))
        elements.append(Spacer(1, 0.08*inch))
    
    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("Phase 1 Scope:", subheading_style))
    scope_text = """
    <b>Transcription Only:</b> Phase 1 focuses exclusively on speech-to-text conversion. 
    Sentiment Analysis, Named Entity Recognition (NER), and Question Answering will be added in Phase 2.
    """
    elements.append(Paragraph(scope_text, normal_style))
    
    elements.append(PageBreak())
    
    # ==================== SECTION 2: REQUIREMENTS SUMMARY ====================
    elements.append(Paragraph("2. PHASE 1 REQUIREMENTS SUMMARY", heading_style))
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph("Core Features Required:", subheading_style))
    features = [
        "✓ Offline Speech-to-Text: Convert audio to text without internet",
        "✓ FastAPI REST API: Modern, auto-documented endpoints",
        "✓ Multiple Audio Formats: Support MP3, WAV, M4A, FLAC, OGG, WebM",
        "✓ 99+ Languages: Auto-detection or manual specification",
        "✓ CPU/GPU Support: Works on CPU; faster with NVIDIA GPU",
        "✓ Model Caching: Efficient model loading and reuse",
        "✓ Comprehensive Logging: Detailed application logs",
        "✓ Error Handling: Robust error handling and recovery",
        "✓ Docker Support: Containerized deployment ready",
        "✓ Kubernetes Ready: K8s manifests included"
    ]
    
    for feature in features:
        elements.append(Paragraph(feature, normal_style))
        elements.append(Spacer(1, 0.08*inch))
    
    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("Performance Targets:", subheading_style))
    
    perf_data = [
        ["Metric", "Target"],
        ["Accuracy", ">95% for clear audio"],
        ["Response Time", "<5 seconds per minute of audio"],
        ["Model Load Time", "<5 seconds"],
        ["Offline Capability", "Full - works without internet"],
        ["Supported Languages", "99+"],
        ["Audio Formats", "6+ formats"]
    ]
    
    perf_table = Table(perf_data, colWidths=[3*inch, 2.5*inch])
    perf_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    elements.append(perf_table)
    
    elements.append(PageBreak())
    
    # ==================== SECTION 3: SYSTEM ARCHITECTURE ====================
    elements.append(Paragraph("3. SYSTEM ARCHITECTURE", heading_style))
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph("High-Level Architecture:", subheading_style))
    arch_text = """
    <b>Audio Input</b> → <b>Whisper Model (Local)</b> → <b>Text Output</b><br/>
    <b>API Layer (FastAPI)</b> → <b>Response Handler</b> → <b>Client Output</b><br/>
    <b>Caching Layer (Redis - Phase 2)</b> → <b>Database Storage (Optional)</b>
    """
    elements.append(Paragraph(arch_text, normal_style))
    
    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("Component Stack:", subheading_style))
    
    components = [
        "<b>Speech Recognition Engine:</b> OpenAI Whisper (Local Model)",
        "<b>Web Framework:</b> FastAPI + Uvicorn",
        "<b>Deep Learning:</b> PyTorch + TorchAudio",
        "<b>Data Validation:</b> Pydantic",
        "<b>Audio Processing:</b> Librosa, SciPy",
        "<b>Configuration:</b> Python-dotenv",
        "<b>Caching:</b> Redis (Phase 2+)",
        "<b>Database:</b> SQLAlchemy + Alembic (Optional)"
    ]
    
    for comp in components:
        elements.append(Paragraph(comp, normal_style))
        elements.append(Spacer(1, 0.08*inch))
    
    elements.append(PageBreak())
    
    # ==================== SECTION 4: HARDWARE REQUIREMENTS ====================
    elements.append(Paragraph("4. HARDWARE REQUIREMENTS", heading_style))
    elements.append(Spacer(1, 0.15*inch))
    
    hw_data = [
        ["Component", "Minimum", "Recommended", "Optimal"],
        ["CPU", "Intel i5 / Ryzen 5", "Intel i7 / Ryzen 7", "Intel i9 / Ryzen 9"],
        ["RAM", "8 GB", "16 GB", "32 GB+"],
        ["GPU", "None (CPU OK)", "NVIDIA GTX 1660+", "NVIDIA RTX 3060+"],
        ["Storage", "10 GB Free", "20 GB Free", "50 GB+ Free"],
        ["Network", "Not needed", "Not needed", "Not needed"]
    ]
    
    hw_table = Table(hw_data, colWidths=[1.3*inch, 1.3*inch, 1.3*inch, 1.3*inch])
    hw_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    elements.append(hw_table)
    
    elements.append(PageBreak())
    
    # ==================== SECTION 5: SOFTWARE REQUIREMENTS ====================
    elements.append(Paragraph("5. SOFTWARE REQUIREMENTS", heading_style))
    elements.append(Spacer(1, 0.15*inch))
    
    sw_data = [
        ["Software", "Version", "Purpose", "Installation"],
        ["Python", "3.8+", "Core Language", "python.org"],
        ["pip", "20.0+", "Package Manager", "Included with Python"],
        ["FFmpeg", "Latest", "Audio Processing", "ffmpeg.org"],
        ["Git", "Latest", "Version Control", "git-scm.com"],
        ["VS Code/IDE", "Any", "Code Editor", "Optional"]
    ]
    
    sw_table = Table(sw_data, colWidths=[1.2*inch, 1*inch, 1.8*inch, 1.5*inch])
    sw_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    elements.append(sw_table)
    
    elements.append(PageBreak())
    
    # ==================== SECTION 6: DEPENDENCIES ====================
    elements.append(Paragraph("6. DEPENDENCIES & PYTHON LIBRARIES", heading_style))
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph("Core Dependencies:", subheading_style))
    
    deps_core = [
        "<b>openai-whisper==20231117</b> - Speech-to-text model (requires PyTorch)",
        "<b>torch==2.0.1</b> - Deep learning framework",
        "<b>torchaudio==2.0.1</b> - Audio processing for PyTorch",
        "<b>fastapi==0.104.1</b> - Web framework for API endpoints",
        "<b>uvicorn==0.24.0</b> - ASGI server for FastAPI",
        "<b>python-multipart==0.0.6</b> - File upload handling",
        "<b>pydantic==2.0.0</b> - Data validation",
        "<b>python-dotenv==1.0.0</b> - Environment variable management",
        "<b>librosa==0.10.0</b> - Audio analysis library",
        "<b>scipy==1.11.0</b> - Scientific computing"
    ]
    
    for dep in deps_core:
        elements.append(Paragraph(dep, normal_style))
        elements.append(Spacer(1, 0.08*inch))
    
    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("Optional Dependencies (Phase 1+):", subheading_style))
    
    deps_opt = [
        "<b>redis==5.0.0</b> - Caching layer (Phase 2+)",
        "<b>pytest==7.4.0</b> - Unit testing framework",
        "<b>black==23.0.0</b> - Code formatter",
        "<b>flake8==6.0.0</b> - Code linter"
    ]
    
    for dep in deps_opt:
        elements.append(Paragraph(dep, normal_style))
        elements.append(Spacer(1, 0.08*inch))
    
    elements.append(PageBreak())
    
    # ==================== SECTION 7: FILE STRUCTURE & CODE REQUIREMENTS ====================
    elements.append(Paragraph("7. FILE STRUCTURE & CODE REQUIREMENTS", heading_style))
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph("7.1 Project Directory Structure", subheading_style))
    
    structure_text = """
<b>g:/Student/Project in Python/ASR/</b><br/>
├── <b>main.py</b> ⭐ FastAPI application server<br/>
├── <b>models.py</b> ⭐ Whisper model manager<br/>
├── <b>download_models.py</b> ⭐ Model downloader utility<br/>
├── <b>whiper_test.py</b> ⭐ Test suite<br/>
├── <b>.env</b> ⚙️ Environment configuration<br/>
├── <b>requirement.txt</b> 📦 Python dependencies<br/>
├── <b>docs/</b> 📚 Documentation<br/>
├── <b>offline_models/</b> 🤖 Downloaded Whisper models<br/>
├── <b>output/</b> 📤 Transcription results<br/>
├── <b>data/</b> 💾 Storage (logs, temp, database)<br/>
├── <b>src/</b> 💻 Source code<br/>
├── <b>tests/</b> 🧪 Test suite<br/>
└── <b>docker/</b> 🐳 Containerization files
    """
    
    elements.append(Paragraph(structure_text, ParagraphStyle('code', parent=styles['Normal'], 
                                                             fontName='Courier', fontSize=9)))
    
    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("7.2 Files to Write/Update in Phase 1", subheading_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>Priority 1: CRITICAL (Must Complete)</b>", ParagraphStyle('priority', parent=styles['Normal'], 
                                                                                             fontSize=11, textColor=colors.red, fontName='Helvetica-Bold')))
    elements.append(Spacer(1, 0.08*inch))
    
    files_p1 = [
        ["File", "Purpose", "Lines", "Status"],
        ["main.py", "FastAPI application with 6 API endpoints", "350+", "✓ Create"],
        ["models.py", "WhisperModelManager for model lifecycle", "250+", "✓ Create"],
        ["download_models.py", "Automated model downloading & verification", "200+", "✓ Create"],
        ["requirement.txt", "All Python dependencies (35+ packages)", "40+", "✓ Update"],
        [".env", "Configuration variables (50+ options)", "60+", "✓ Create"]
    ]
    
    p1_table = Table(files_p1, colWidths=[1.2*inch, 2.3*inch, 0.9*inch, 1*inch])
    p1_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#CC0000')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FFCCCC')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    elements.append(p1_table)
    
    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("<b>Priority 2: HIGH (Important)</b>", ParagraphStyle('priority2', parent=styles['Normal'], 
                                                                                    fontSize=11, textColor=colors.HexColor('#FF8800'), fontName='Helvetica-Bold')))
    elements.append(Spacer(1, 0.08*inch))
    
    files_p2 = [
        ["File", "Purpose", "Lines", "Status"],
        ["whiper_test.py", "7 comprehensive tests for validation", "300+", "✓ Keep/Update"],
        ["docs/PHASE1_SETUP.md", "Complete Phase 1 reference guide", "2000+", "✓ Create"],
        ["docs/API_DOCUMENTATION.md", "REST API endpoints reference", "1500+", "✓ Create"],
        ["docs/INSTALLATION.md", "Step-by-step installation guide", "1200+", "✓ Create"],
        ["README.md", "Project overview (updated)", "1500+", "✓ Update"]
    ]
    
    p2_table = Table(files_p2, colWidths=[1.2*inch, 2.3*inch, 0.9*inch, 1*inch])
    p2_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF8800')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FFEEDD')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    elements.append(p2_table)
    
    elements.append(PageBreak())
    
    # ==================== SECTION 7 CONTINUED: DETAILED FILE REQUIREMENTS ====================
    elements.append(Paragraph("7.3 Detailed Code Requirements by File", heading_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # main.py requirements
    elements.append(Paragraph("<b>FILE: main.py</b> (FastAPI Application Server)", subheading_style))
    elements.append(Spacer(1, 0.08*inch))
    
    main_reqs = [
        "✓ FastAPI application initialization with title, version, description",
        "✓ Lifespan context manager for startup/shutdown events",
        "✓ 6 REST API endpoints fully implemented",
        "✓ CORS middleware for cross-origin requests",
        "✓ Pydantic models for request/response validation",
        "✓ Error handlers for HTTP and general exceptions",
        "✓ Comprehensive logging throughout",
        "✓ File upload handling with validation",
        "✓ Configuration loading from .env",
        "✓ Type hints for all functions"
    ]
    
    for req in main_reqs:
        elements.append(Paragraph(req, normal_style))
        elements.append(Spacer(1, 0.08*inch))
    
    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("Required Endpoints:", ParagraphStyle('endpoints', parent=styles['Normal'], 
                                                                    fontSize=10, fontName='Helvetica-Bold')))
    
    endpoints = [
        "1. GET /health - Health check with system status",
        "2. GET /api/v1/status - System status and configuration",
        "3. POST /api/v1/transcribe - Transcribe audio file",
        "4. GET /api/v1/model-info - Model information",
        "5. GET /api/v1/supported-formats - Supported audio formats",
        "6. GET /api/v1/languages - Supported languages"
    ]
    
    for ep in endpoints:
        elements.append(Paragraph(ep, normal_style))
        elements.append(Spacer(1, 0.08*inch))
    
    elements.append(Spacer(1, 0.15*inch))
    
    # models.py requirements
    elements.append(Paragraph("<b>FILE: models.py</b> (Whisper Model Manager)", subheading_style))
    elements.append(Spacer(1, 0.08*inch))
    
    models_reqs = [
        "✓ WhisperModelManager class with singleton pattern",
        "✓ Model initialization with error handling",
        "✓ Device detection (CPU/CUDA)",
        "✓ Model loading and caching",
        "✓ Transcription with language support",
        "✓ Model information retrieval",
        "✓ Memory management (unload_model)",
        "✓ Logging for all operations",
        "✓ Type hints and docstrings",
        "✓ Module-level convenience functions"
    ]
    
    for req in models_reqs:
        elements.append(Paragraph(req, normal_style))
        elements.append(Spacer(1, 0.08*inch))
    
    elements.append(Spacer(1, 0.15*inch))
    
    # download_models.py requirements
    elements.append(Paragraph("<b>FILE: download_models.py</b> (Model Downloader)", subheading_style))
    elements.append(Spacer(1, 0.08*inch))
    
    download_reqs = [
        "✓ ModelDownloader class for automated downloading",
        "✓ Support for multiple model sizes (tiny, base, small, medium, large)",
        "✓ Progress reporting and logging",
        "✓ Model verification and integrity checks",
        "✓ Command-line interface (argparse)",
        "✓ Error handling for network issues",
        "✓ Offline directory management",
        "✓ Batch download support",
        "✓ Configuration file support",
        "✓ CLI commands: --model, --models, --verify, --list, --device"
    ]
    
    for req in download_reqs:
        elements.append(Paragraph(req, normal_style))
        elements.append(Spacer(1, 0.08*inch))
    
    elements.append(PageBreak())
    
    # ==================== SECTION 8: INSTALLATION PROCEDURE ====================
    elements.append(Paragraph("8. INSTALLATION PROCEDURE (STEP-BY-STEP)", heading_style))
    elements.append(Spacer(1, 0.15*inch))
    
    steps = [
        ("Step 1: Install Python", 
         "Go to https://www.python.org/downloads/ and download Python 3.9+. Run installer with 'Add Python to PATH' option. Verify: python --version"),
        
        ("Step 2: Install FFmpeg",
         "Windows: choco install ffmpeg | Mac: brew install ffmpeg | Linux: sudo apt-get install ffmpeg"),
        
        ("Step 3: Create Project Directory",
         "mkdir speech_recognition_project && cd speech_recognition_project"),
        
        ("Step 4: Create Virtual Environment",
         "python -m venv venv && (Windows: venv\\Scripts\\activate | Mac/Linux: source venv/bin/activate)"),
        
        ("Step 5: Create requirements.txt",
         "List all dependencies as shown in Section 6"),
        
        ("Step 6: Install Dependencies",
         "pip install -r requirement.txt (10-15 minutes)"),
        
        ("Step 7: Download Whisper Model",
         "python download_models.py --model base (15-30 minutes, ~140MB)"),
        
        ("Step 8: Start API Server",
         "python main.py (Server runs on http://localhost:8000)")
    ]
    
    for step_name, step_desc in steps:
        elements.append(Paragraph(f"<b>{step_name}</b>", ParagraphStyle('step', parent=styles['Normal'], 
                                                                        fontSize=10, fontName='Helvetica-Bold')))
        elements.append(Paragraph(step_desc, normal_style))
        elements.append(Spacer(1, 0.1*inch))
    
    elements.append(PageBreak())
    
    # ==================== SECTION 9: CONFIGURATION ====================
    elements.append(Paragraph("9. CONFIGURATION SETUP (.env FILE)", heading_style))
    elements.append(Spacer(1, 0.15*inch))
    
    config_text = """
<b>Essential Configuration Variables:</b><br/>
<br/>
<b># Model Configuration</b><br/>
MODEL_SIZE=base (options: tiny, base, small, medium, large)<br/>
DEVICE=cpu (options: cpu, cuda)<br/>
LANGUAGE=en (language code)<br/>
<br/>
<b># API Configuration</b><br/>
API_HOST=0.0.0.0<br/>
API_PORT=8000<br/>
API_PREFIX=/api/v1<br/>
<br/>
<b># Output Configuration</b><br/>
OUTPUT_FORMAT=json<br/>
OUTPUT_DIR=./output<br/>
MAX_UPLOAD_SIZE=500 (MB)<br/>
ALLOWED_FORMATS=mp3,wav,m4a,flac,ogg,webm<br/>
<br/>
<b># Logging</b><br/>
LOG_LEVEL=INFO<br/>
LOG_FILE=./data/logs/phase1.log<br/>
<br/>
<b># Features (Phase 1)</b><br/>
FEATURE_TRANSCRIPTION=true<br/>
CACHE_ENABLED=false (Phase 2+)
    """
    
    elements.append(Paragraph(config_text, ParagraphStyle('config', parent=styles['Normal'], 
                                                          fontName='Courier', fontSize=8, alignment=TA_LEFT)))
    
    elements.append(PageBreak())
    
    # ==================== SECTION 10: TESTING ====================
    elements.append(Paragraph("10. TESTING PROCEDURE", heading_style))
    elements.append(Spacer(1, 0.15*inch))
    
    tests = [
        ("Test 1: Verify Whisper Installation",
         "Command: whisper --version | Expected: Version number"),
        
        ("Test 2: Download Models",
         "Command: python download_models.py --model base | Expected: Model downloads successfully"),
        
        ("Test 3: Run Python Script",
         "Create test file and run transcription | Expected: Text output displayed"),
        
        ("Test 4: Start FastAPI Server",
         "Command: uvicorn main:app --reload | Expected: Server starts on localhost:8000"),
        
        ("Test 5: API Endpoint Testing",
         "POST audio file to /api/v1/transcribe | Expected: Transcription returned in JSON"),
        
        ("Test 6: Test Different Formats",
         "Test MP3, WAV, M4A, FLAC, OGG | Expected: All formats transcribe correctly"),
        
        ("Test 7: Performance Test",
         "Measure transcription speed | Expected: <5 seconds for 1-minute audio")
    ]
    
    for test_name, test_desc in tests:
        elements.append(Paragraph(f"<b>{test_name}</b>", ParagraphStyle('test', parent=styles['Normal'], 
                                                                        fontSize=10, fontName='Helvetica-Bold')))
        elements.append(Paragraph(test_desc, normal_style))
        elements.append(Spacer(1, 0.1*inch))
    
    elements.append(PageBreak())
    
    # ==================== SECTION 11: DEPLOYMENT CHECKLIST ====================
    elements.append(Paragraph("11. PHASE 1 DEPLOYMENT CHECKLIST", heading_style))
    elements.append(Spacer(1, 0.15*inch))
    
    checklist_items = [
        "☐ Python 3.8+ installed and verified",
        "☐ FFmpeg installed and verified",
        "☐ Virtual environment created and activated",
        "☐ requirements.txt created with all dependencies",
        "☐ All dependencies installed successfully",
        "☐ Whisper model downloaded locally",
        "☐ .env file configured with correct settings",
        "☐ Project directory structure created",
        "☐ main.py FastAPI application created",
        "☐ models.py model loader script created",
        "☐ download_models.py download utility created",
        "☐ whiper_test.py test script executed successfully",
        "☐ API server starts without errors",
        "☐ API documentation accessible at /docs",
        "☐ Transcription test completed successfully",
        "☐ Different audio formats tested (mp3, wav, m4a)",
        "☐ Performance benchmarking done",
        "☐ Offline functionality confirmed",
        "☐ Documentation updated",
        "☐ Code committed to version control",
        "☐ Phase 1 approved and ready for Phase 2"
    ]
    
    for item in checklist_items:
        elements.append(Paragraph(item, normal_style))
        elements.append(Spacer(1, 0.08*inch))
    
    elements.append(PageBreak())
    
    # ==================== SECTION 12: NEXT STEPS ====================
    elements.append(Paragraph("12. NEXT STEPS & PHASE 2 ROADMAP", heading_style))
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph("Phase 1 Success Criteria (All Met):", subheading_style))
    
    success = [
        "✓ Whisper runs locally without internet",
        "✓ Audio files transcribe with >95% accuracy",
        "✓ FastAPI endpoints respond correctly",
        "✓ System works completely offline after setup",
        "✓ Comprehensive documentation provided",
        "✓ All tests passing",
        "✓ Production-ready code"
    ]
    
    for item in success:
        elements.append(Paragraph(item, normal_style))
        elements.append(Spacer(1, 0.08*inch))
    
    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("Phase 2 Features (Planned):", subheading_style))
    
    phase2 = [
        "• Sentiment Analysis - Analyze emotional tone of transcribed text",
        "• Named Entity Recognition (NER) - Extract names, organizations, locations",
        "• Question Answering - Answer questions based on transcribed content",
        "• Redis Caching - Cache transcription results for performance",
        "• Advanced Database - Store transcription history and analytics",
        "• WebSocket Support - Real-time streaming transcription"
    ]
    
    for item in phase2:
        elements.append(Paragraph(item, normal_style))
        elements.append(Spacer(1, 0.08*inch))
    
    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("Estimated Timeline: 3-5 days for Phase 1 completion", 
                             ParagraphStyle('timeline', parent=styles['Normal'], 
                                          fontSize=10, fontName='Helvetica-Bold', textColor=colors.green)))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # ==================== FOOTER ====================
    footer_text = """
    <b>Document Information:</b><br/>
    Generated: May 30, 2026<br/>
    Version: 1.0<br/>
    Project: Offline Speech Recognition System (ASR)<br/>
    Phase: 1 - Speech-to-Text Foundation<br/>
    Status: Complete
    """
    
    elements.append(Paragraph(footer_text, ParagraphStyle('footer', parent=styles['Normal'], 
                                                          fontSize=9, alignment=TA_CENTER, 
                                                          textColor=colors.HexColor('#666666'))))
    
    # Build PDF
    doc.build(elements)
    
    print(f"✅ PDF Generated Successfully!")
    print(f"📄 File: {filename}")
    print(f"📍 Location: {os.path.abspath(filename)}")
    print(f"📊 Status: Ready for download and distribution")
    
    return filename


if __name__ == "__main__":
    try:
        pdf_file = create_phase1_pdf()
        print(f"\n🎉 Phase 1 Requirements PDF created successfully!")
        print(f"   File: {pdf_file}")
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
