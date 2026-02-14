#!/usr/bin/env python3
"""
מודול ליצירת PDF מעוצב
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from datetime import datetime
import re


def create_styled_pdf(summary: str, filename: str = None) -> str:
    """
    יוצר PDF מעוצב מהסיכום
    
    Args:
        summary: טקסט הסיכום
        filename: שם הקובץ (אופציונלי)
    
    Returns:
        נתיב לקובץ שנוצר
    """
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"ai_news_digest_{timestamp}.pdf"
    
    # יצירת המסמך
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
    
    # סטיילים מותאמים אישית
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1e40af'),  # כחול כהה
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#64748b'),  # אפור
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#0f172a'),  # כמעט שחור
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    content_style = ParagraphStyle(
        'Content',
        parent=styles['BodyText'],
        fontSize=11,
        leading=18,
        textColor=colors.HexColor('#1e293b'),
        alignment=TA_RIGHT,
        rightIndent=0,
        leftIndent=0
    )
    
    # כותרת ראשית
    title = Paragraph("📰 סיכום חדשות AI", title_style)
    elements.append(title)
    
    # תאריך
    current_date = datetime.now().strftime('%d/%m/%Y - %H:%M')
    date_para = Paragraph(f"נוצר בתאריך: {current_date}", subtitle_style)
    elements.append(date_para)
    
    # קו מפריד
    elements.append(Spacer(1, 0.3*inch))
    
    # עיבוד התוכן
    lines = summary.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if not line or line == '---':
            elements.append(Spacer(1, 0.15*inch))
            continue
        
        # זיהוי כותרות
        if line.startswith('##'):
            # כותרת מדרגה 2
            text = line.replace('##', '').strip()
            # הסרת אימוג'י עבור PDF
            text = re.sub(r'[^\w\s\u0590-\u05FF-]', '', text)
            para = Paragraph(text, section_title_style)
            elements.append(para)
        
        elif line.startswith('#'):
            # כותרת ראשית (כבר יש לנו)
            continue
        
        elif line.startswith('**') and line.endswith('**'):
            # טקסט מודגש
            text = line.replace('**', '').strip()
            bold_style = ParagraphStyle(
                'Bold',
                parent=content_style,
                fontName='Helvetica-Bold'
            )
            para = Paragraph(text, bold_style)
            elements.append(para)
        
        elif line.startswith('- ') or line.startswith('* '):
            # נקודות
            text = '• ' + line[2:].strip()
            para = Paragraph(text, content_style)
            elements.append(para)
        
        else:
            # טקסט רגיל
            # הסרת markdown
            text = line.replace('**', '')
            if text:
                para = Paragraph(text, content_style)
                elements.append(para)
                elements.append(Spacer(1, 0.1*inch))
    
    # פוטר
    elements.append(Spacer(1, 0.5*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#94a3b8'),
        alignment=TA_CENTER
    )
    footer = Paragraph("נוצר אוטומטית על ידי AI News Digest System", footer_style)
    elements.append(footer)
    
    # בניית ה-PDF
    doc.build(elements)
    
    print(f"📄 PDF נוצר בהצלחה: {filename}")
    return filename


# =====================================================
# שימוש לדוגמה
# =====================================================

if __name__ == "__main__":
    # דוגמה לשימוש
    sample_summary = """# 📰 סיכום חדשות AI - 14/02/2026

## 🆕 מוצרים ושירותים חדשים

**OpenAI השיקה GPT-5**
OpenAI הכריזה על GPT-5, המודל החדש שלה שמציג שיפור משמעותי ביכולות הנמקה מתמטית. המודל זמין כעת ל-API users.

## 🔬 מחקר ופיתוח

**פריצת דרך בהבנת LLMs**
חוקרים מסטנפורד פרסמו מחקר חדש על המבנה הפנימי של מודלי שפה גדולים.

---
**מקורות:** TechCrunch AI, VentureBeat AI, MIT Technology Review
"""
    
    create_styled_pdf(sample_summary, "example_digest.pdf")
