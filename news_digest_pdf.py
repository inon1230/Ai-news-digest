#!/usr/bin/env python3
"""
הרחבה: יצירת PDF מעוצב
גרסה שמייצרת PDF מעוצב במקום קובץ טקסט רגיל
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from news_digest import fetch_news_from_sources, analyze_and_summarize_with_claude


def create_pdf_digest(summary: str, filename: str = None) -> str:
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
        rightMargin=1*inch,
        leftMargin=1*inch,
        topMargin=1*inch,
        bottomMargin=1*inch
    )
    
    # רשימת האלמנטים שיהיו ב-PDF
    elements = []
    
    # יצירת סטיילים
    styles = getSampleStyleSheet()
    
    # סטייל לכותרת ראשית
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#1e3a8a',
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # סטייל לתאריך
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=12,
        textColor='#6b7280',
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    # סטייל לתוכן
    content_style = ParagraphStyle(
        'ContentStyle',
        parent=styles['BodyText'],
        fontSize=11,
        leading=16,
        textColor='#1f2937',
        alignment=TA_RIGHT  # יישור לימין לעברית
    )
    
    # הוספת כותרת
    title = Paragraph("📰 AI News Digest", title_style)
    elements.append(title)
    
    # הוספת תאריך
    current_date = datetime.now().strftime('%d/%m/%Y - %H:%M')
    date_para = Paragraph(f"נוצר בתאריך: {current_date}", date_style)
    elements.append(date_para)
    
    elements.append(Spacer(1, 0.3*inch))
    
    # עיבוד הטקסט - המרת Markdown לפורמט PDF
    lines = summary.split('\n')
    for line in lines:
        if not line.strip():
            elements.append(Spacer(1, 0.1*inch))
            continue
        
        # זיהוי כותרות (מתחילות ב-#)
        if line.startswith('###'):
            heading_style = ParagraphStyle(
                'Heading3',
                parent=styles['Heading3'],
                fontSize=12,
                textColor='#374151',
                spaceAfter=10
            )
            text = line.replace('###', '').strip()
            elements.append(Paragraph(text, heading_style))
        elif line.startswith('##'):
            heading_style = ParagraphStyle(
                'Heading2',
                parent=styles['Heading2'],
                fontSize=14,
                textColor='#1f2937',
                spaceAfter=12
            )
            text = line.replace('##', '').strip()
            elements.append(Paragraph(text, heading_style))
        elif line.startswith('#'):
            text = line.replace('#', '').strip()
            elements.append(Paragraph(text, title_style))
        else:
            # טקסט רגיל
            # המרת תווים מיוחדים
            text = line.replace('**', '<b>').replace('**', '</b>')
            text = text.replace('*', '<i>').replace('*', '</i>')
            elements.append(Paragraph(text, content_style))
    
    # הוספת פוטר
    elements.append(Spacer(1, 0.5*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor='#9ca3af',
        alignment=TA_CENTER
    )
    footer = Paragraph("נוצר אוטומטית על ידי AI News Digest System", footer_style)
    elements.append(footer)
    
    # בניית ה-PDF
    doc.build(elements)
    
    print(f"📄 PDF נוצר בהצלחה: {filename}")
    return filename


def main():
    """
    Main function עם יצירת PDF
    """
    print("🚀 AI News Digest + PDF - מתחיל...")
    
    # שלב 1: איסוף חדשות
    articles = fetch_news_from_sources()
    
    if not articles:
        print("⚠️  לא נמצאו חדשות חדשות")
        return
    
    # שלב 2: סיכום
    summary = analyze_and_summarize_with_claude(articles)
    
    # שלב 3: יצירת PDF
    pdf_file = create_pdf_digest(summary)
    
    print(f"✅ התהליך הושלם! PDF נוצר: {pdf_file}")


if __name__ == "__main__":
    main()
