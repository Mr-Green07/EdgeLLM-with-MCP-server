#!/usr/bin/env python3
"""
Generate PDF from all documentation files using reportlab
"""

import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import re

def clean_markdown(text):
    """Convert markdown syntax to plain text for reportlab"""
    text = re.sub(r'```[a-z]*\n(.*?)\n```', r'\1', text, flags=re.DOTALL)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'__([^_]+)__', r'\1', text)
    text = re.sub(r'_([^_]+)_', r'\1', text)
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    return text.strip()

def parse_markdown_to_reportlab(content, styles):
    """Parse markdown and convert to reportlab elements"""
    elements = []
    lines = content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if not line.strip():
            elements.append(Spacer(1, 0.05*inch))
            i += 1
            continue
        
        # H1 headings
        if line.startswith('# '):
            text = line.replace('# ', '').strip()
            style = ParagraphStyle(
                'CustomH1',
                parent=styles['Heading1'],
                fontSize=20,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=12,
                spaceBefore=12
            )
            elements.append(Paragraph(text, style))
            elements.append(Spacer(1, 0.15*inch))
            i += 1
            continue
        
        # H2 headings
        if line.startswith('## '):
            text = line.replace('## ', '').strip()
            style = ParagraphStyle(
                'CustomH2',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#34495e'),
                spaceAfter=10,
                spaceBefore=10
            )
            elements.append(Paragraph(text, style))
            elements.append(Spacer(1, 0.1*inch))
            i += 1
            continue
        
        # H3 headings
        if line.startswith('### '):
            text = line.replace('### ', '').strip()
            style = ParagraphStyle(
                'CustomH3',
                parent=styles['Heading3'],
                fontSize=13,
                textColor=colors.HexColor('#7f8c8d'),
                spaceAfter=8,
                spaceBefore=8
            )
            elements.append(Paragraph(text, style))
            elements.append(Spacer(1, 0.08*inch))
            i += 1
            continue
        
        # Code blocks
        if line.startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code_lines.append(lines[i])
                i += 1
            
            code_text = '\n'.join(code_lines)
            code_style = ParagraphStyle(
                'Code',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.HexColor('#2c3e50'),
                backColor=colors.HexColor('#ecf0f1'),
                leftIndent=20,
                rightIndent=20,
                spaceAfter=8,
                family='Courier'
            )
            
            for code_line in code_text.split('\n'):
                if code_line.strip():
                    elements.append(Paragraph(code_line, code_style))
            
            elements.append(Spacer(1, 0.1*inch))
            i += 1
            continue
        
        # Regular paragraphs
        if line.strip():
            clean_text = clean_markdown(line)
            if clean_text:
                style = ParagraphStyle(
                    'Normal',
                    parent=styles['Normal'],
                    fontSize=10,
                    alignment=TA_JUSTIFY,
                    spaceAfter=6,
                    leading=13
                )
                elements.append(Paragraph(clean_text, style))
        
        i += 1
    
    return elements

def generate_pdf():
    """Generate PDF from all documentation files"""
    
    docs_folder = Path("docs")
    
    doc_files = [
        "INDEX.md",
        "QUICK_START.md",
        "COMPLETE_GUIDE.md",
        "COMPONENT_OVERVIEW.md",
        "PRACTICAL_EXAMPLES.md",
        "architecture/overview.md",
        "architecture/components.md",
        "architecture/data_flow.md",
        "architecture/state_machine.md",
        "api/rest_api.md",
        "deployment/installation.md",
        "deployment/configuration.md",
        "deployment/docker.md",
        "deployment/kubernetes.md",
        "development/setup.md",
        "development/coding_standards.md",
        "development/testing.md",
        "development/contributing.md",
        "performance/benchmarks.md",
        "performance/optimization.md",
        "performance/resource_usage.md",
        "user_guide/commands.md",
        "user_guide/customization.md",
        "user_guide/troubleshooting.md",
    ]
    
    print("PDF GENERATION")
    print("=" * 60)
    print("📄 Generating PDF from documentation files...")
    print(f"📁 Documentation folder: {docs_folder}")
    print(f"📊 Total files to include: {len(doc_files)}")
    print()
    
    styles = getSampleStyleSheet()
    
    output_file = "Voice_Assistant_Complete_Documentation.pdf"
    doc = SimpleDocTemplate(
        output_file,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
        title="Voice Assistant Platform - Complete Documentation"
    )
    
    story = []
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=28,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#7f8c8d'),
        alignment=TA_CENTER,
        spaceAfter=24
    )
    
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("Voice Assistant Platform", title_style))
    story.append(Paragraph("Complete Documentation", subtitle_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Comprehensive Guide to Voice AI System", subtitle_style))
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("Generated: May 2024", ParagraphStyle('Normal', parent=styles['Normal'], fontSize=10, alignment=TA_CENTER)))
    story.append(PageBreak())
    
    story.append(Paragraph("Table of Contents", styles['Heading1']))
    story.append(Spacer(1, 0.2*inch))
    
    toc_style = ParagraphStyle(
        'TOC',
        parent=styles['Normal'],
        fontSize=9,
        leftIndent=20,
        spaceAfter=4
    )
    
    for i, doc_file in enumerate(doc_files, 1):
        title = doc_file.replace(".md", "").replace("/", " > ").replace("_", " ").title()
        story.append(Paragraph(f"{i}. {title}", toc_style))
    
    story.append(PageBreak())
    
    file_count = 0
    for doc_file in doc_files:
        filepath = docs_folder / doc_file
        
        if filepath.exists():
            file_count += 1
            print(f"✅ Processing: {doc_file} ({file_count}/{len(doc_files)})")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) > 2:
                    content = parts[2]
            
            elements = parse_markdown_to_reportlab(content, styles)
            story.extend(elements)
            story.append(PageBreak())
        else:
            print(f"⚠️  Skipped: {doc_file} (not found)")
    
    print()
    print(f"🔄 Building PDF with {file_count} files...")
    print("This may take a moment...")
    print()
    
    try:
        doc.build(story)
        
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file) / (1024 * 1024)
            print("=" * 60)
            print("✅ ✅ ✅ PDF GENERATED SUCCESSFULLY! ✅ ✅ ✅")
            print("=" * 60)
            print()
            print(f"📄 File Name: {output_file}")
            print(f"📊 File Size: {file_size:.2f} MB")
            print(f"📍 Location: {os.path.abspath(output_file)}")
            print()
            print("✨ The PDF is ready to:")
            print("   ✓ View on your computer")
            print("   ✓ Share with others")
            print("   ✓ Print out")
            print()
            return True
        else:
            print("❌ Error: PDF file was not created")
            return False
    
    except Exception as e:
        print(f"❌ Error building PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = generate_pdf()
    sys.exit(0 if success else 1)
