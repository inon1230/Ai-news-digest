#!/usr/bin/env python3
"""
PDF Generator for AI News Digest
Creates beautifully formatted PDF reports
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from datetime import datetime
import re


def create_pdf_digest(summary: str, filename: str = None) -> str:
    """
    Creates a beautifully formatted PDF from the summary
    
    Args:
        summary: The text summary
        filename: Output filename (optional)
    
    Returns:
        Path to the created file
    """
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"ai_news_digest_{timestamp}.pdf"
    
    print(f"Creating PDF: {filename}")
    
    # Create document
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=26,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=25,
        alignment=TA_CENTER
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#dc2626'),
        spaceAfter=10,
        spaceBefore=18,
        fontName='Helvetica-Bold'
    )
    
    content_style = ParagraphStyle(
        'Content',
        parent=styles['BodyText'],
        fontSize=10,
        leading=16,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=8,
        alignment=TA_RIGHT
    )
    
    # Build document
    
    # Title
    title = Paragraph("AI News Digest", title_style)
    elements.append(title)
    
    # Date
    current_date = datetime.now().strftime('%d/%m/%Y')
    date_para = Paragraph(f"Daily Summary - {current_date}", subtitle_style)
    elements.append(date_para)
    
    # Separator
    elements.append(Spacer(1, 0.2*inch))
    
    # Process content
    lines = summary.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if not line:
            elements.append(Spacer(1, 0.1*inch))
            continue
        
        # Skip separators
        if line == '---' or line.startswith('---'):
            elements.append(Spacer(1, 0.2*inch))
            continue
        
        # Main title (# )
        if line.startswith('# '):
            continue  # Already have title
        
        # Section title (## )
        elif line.startswith('## '):
            text = line.replace('##', '').strip()
            # Remove emojis
            text = re.sub(r'[^\w\s\u0590-\u05FF:()-]', '', text)
            para = Paragraph(text, section_title_style)
            elements.append(para)
        
        # Bold text (**...**)
        elif line.startswith('**') and line.endswith('**'):
            text = line.replace('**', '').strip()
            bold_style = ParagraphStyle(
                'Bold',
                parent=content_style,
                fontName='Helvetica-Bold',
                fontSize=11
            )
            para = Paragraph(text, bold_style)
            elements.append(para)
        
        # Bullet points (- or *)
        elif line.startswith('- ') or line.startswith('* '):
            text = '• ' + line[2:].strip()
            text = text.replace('**', '')
            para = Paragraph(text, content_style)
            elements.append(para)
        
        # Sources
        elif line.startswith('**Sources:**') or line.startswith('**מקורות:**'):
            elements.append(Spacer(1, 0.3*inch))
            sources_style = ParagraphStyle(
                'Sources',
                parent=content_style,
                fontSize=9,
                textColor=colors.HexColor('#64748b'),
                alignment=TA_CENTER
            )
            text = line.replace('**', '')
            para = Paragraph(text, sources_style)
            elements.append(para)
        
        # Regular text
        else:
            text = line.replace('**', '')
            if text:
                para = Paragraph(text, content_style)
                elements.append(para)
    
    # Footer
    elements.append(Spacer(1, 0.5*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#94a3b8'),
        alignment=TA_CENTER
    )
    footer_text = f"Auto-generated - AI News Digest System - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    footer = Paragraph(footer_text, footer_style)
    elements.append(footer)
    
    # Build PDF
    try:
        doc.build(elements)
        print(f"PDF created successfully: {filename}")
        return filename
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return None


if __name__ == "__main__":
    # Test example
    sample = """# AI News Digest - 15/02/2026

## New Products and Services

**OpenAI launched GPT-5**
OpenAI announced GPT-5 with improved capabilities.

## Research and Development

**LLM Understanding Breakthrough**
Researchers discovered new mechanisms.

---
**Sources:** TechCrunch, VentureBeat
"""
    create_pdf_digest(sample, "test.pdf")
