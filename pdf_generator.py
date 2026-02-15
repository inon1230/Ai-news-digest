News digest final pdf · PY
Copy

#!/usr/bin/env python3
"""
AI News Digest - גרסה סופית משודרגת
כולל: טלגרם + PDF + מקורות משופרים
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import feedparser

# יבוא PDF generator
try:
    from pdf_generator import create_pdf_digest
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️  pdf_generator לא זמין - PDF לא ייווצר")

# =====================================================
# הגדרות
# =====================================================

NEWS_SOURCES = {
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "VentureBeat AI": "https://venturebeat.com/category/ai/feed/",
    "MIT Technology Review AI": "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "The Verge AI": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
    "Ars Technica AI": "https://feeds.arstechnica.com/arstechnica/technology-lab",
    "OpenAI Blog": "https://openai.com/blog/rss/",
    "Anthropic News": "https://www.anthropic.com/news/rss.xml",
    "Google AI Blog": "http://googleresearch.blogspot.com/feeds/posts/default",
}

HOURS_BACK = 24
CLAUDE_MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 4000
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"


# =====================================================
# איסוף חדשות
# =====================================================

def fetch_news_from_sources(hours_back: int = HOURS_BACK) -> List[Dict]:
    """אוסף חדשות מכל המקורות"""
    print(f"🔍 מחפש חדשות מ-{hours_back} שעות אחורה...")
    
    all_articles = []
    cutoff_time = datetime.now() - timedelta(hours=hours_back)
    sources_found = set()
    
    for source_name, feed_url in NEWS_SOURCES.items():
        try:
            print(f"  📰 קורא: {source_name}")
            feed = feedparser.parse(feed_url)
            
            count = 0
            for entry in feed.entries[:15]:
                published = entry.get('published_parsed', entry.get('updated_parsed'))
                if published:
                    pub_date = datetime(*published[:6])
                    if pub_date < cutoff_time:
                        continue
                
                article = {
                    'source': source_name,
                    'title': entry.get('title', 'ללא כותרת'),
                    'link': entry.get('link', ''),
                    'summary': entry.get('summary', entry.get('description', '')),
                    'published': pub_date.strftime('%Y-%m-%d %H:%M') if published else 'לא ידוע'
                }
                all_articles.append(article)
                sources_found.add(source_name)
                count += 1
            
            if count > 0:
                print(f"     ✓ נמצאו {count} כתבות")
                
        except Exception as e:
            print(f"  ⚠️  שגיאה בקריאת {source_name}: {e}")
            continue
    
    print(f"\n✅ סה\"כ נמצאו {len(all_articles)} כתבות מ-{len(sources_found)} מקורות\n")
    return all_articles


# =====================================================
# סיכום עם Claude
# =====================================================

def analyze_and_summarize_with_claude(articles: List[Dict]) -> str:
    """שולח את הכתבות ל-Claude לסינון וסיכום"""
    if not articles:
        return "לא נמצאו חדשות חדשות ב-24 שעות האחרונות."
    
    print(f"🤖 שולח {len(articles)} כתבות ל-Claude לניתוח...")
    
    # בניית רשימת המקורות
    sources_list = sorted(set([art['source'] for art in articles]))
    sources_str = ', '.join(sources_list)
    
    articles_text = "\n\n".join([
        f"[{i+1}] {art['source']}\nכותרת: {art['title']}\nתקציר: {art['summary'][:300]}...\nקישור: {art['link']}"
        for i, art in enumerate(articles)
    ])
    
    prompt = f"""אתה עיתונאי טכנולוגיה ישראלי מומחה בתחום הבינה המלאכותית.

קיבלת {len(articles)} כתבות מהמקורות הבאים: {sources_str}

המשימה שלך:
1. קרא את כל הכתבות וזהה את הנושאים החשובים
2. אם כמה מקורות דיווחו על אותו נושא - צלוב את המידע ביניהם
3. סנן החוצה חדשות לא רלוונטיות או משניות
4. כתוב סיכום תמציתי בעברית טבעית ושוטפת
5. חלק לקטגוריות (אם יש תוכן בקטגוריה)

דרישות כתיבה:
- עברית טבעית: "OpenAI השיקה..." (לא "הושק על ידי")
- משפטים קצרים וברורים
- מקסימום 500 מילים
- **חשוב:** בסוף רשום רק את המקורות שבאמת השתמשת בהם

הכתבות:
{articles_text}

פורמט הסיכום:
# 📰 סיכום חדשות AI - {datetime.now().strftime('%d/%m/%Y')}

## 🆕 מוצרים ושירותים חדשים
[אם יש - כתוב את הסיכום. אם אין - דלג על הקטגוריה]

## 🔬 מחקר ופיתוח
[אם יש - כתוב את הסיכום. אם אין - דלג על הקטגוריה]

## 💰 חברות והשקעות
[אם יש - כתוב את הסיכום. אם אין - דלג על הקטגוריה]

## 📌 כללי
[אם יש - כתוב את הסיכום. אם אין - דלג על הקטגוריה]

---
**מקורות זמינים:** {sources_str}
**מקורות בשימוש בפועל:** [רשום כאן רק את המקורות שבאמת השתמשת בהם בסיכום - מופרדים בפסיקים]
"""

    try:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            return "❌ שגיאה: ANTHROPIC_API_KEY לא נמצא"
        
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        payload = {
            "model": CLAUDE_MODEL,
            "max_tokens": MAX_TOKENS,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        print("📡 שולח בקשה ל-Claude API...")
        response = requests.post(ANTHROPIC_API_URL, headers=headers, json=payload, timeout=120)
        
        if response.status_code != 200:
            return f"❌ שגיאה: {response.status_code} - {response.text}"
        
        result = response.json()
        summary = result['content'][0]['text']
        
        print("✅ סיכום הושלם!\n")
        return summary
        
    except Exception as e:
        print(f"❌ שגיאה: {str(e)}")
        return f"שגיאה בעיבוד: {str(e)}"


# =====================================================
# שליחה לטלגרם
# =====================================================

def send_to_telegram(message: str) -> bool:
    """שולח הודעה לטלגרם"""
    TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️  טלגרם לא מוגדר")
        return False
    
    print(f"📱 שולח הודעה לטלגרם...")
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    max_length = 4000
    
    try:
        if len(message) > max_length:
            parts = [message[i:i+max_length] for i in range(0, len(message), max_length)]
            for i, part in enumerate(parts, 1):
                payload = {
                    "chat_id": TELEGRAM_CHAT_ID,
                    "text": f"📄 חלק {i}/{len(parts)}:\n\n{part}",
                    "parse_mode": "Markdown"
                }
                requests.post(url, json=payload, timeout=30)
                print(f"✅ חלק {i}/{len(parts)} נשלח")
        else:
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "Markdown"
            }
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                print("✅ הסיכום נשלח לטלגרם! 🎉")
                return True
            else:
                print(f"❌ שגיאה: {response.status_code}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ שגיאה בשליחה לטלגרם: {e}")
        return False


# =====================================================
# שמירת פלט
# =====================================================

def save_output(summary: str, output_format: str = "txt"):
    """שומר את הסיכום"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if output_format == "txt":
        filename = f"ai_news_digest_{timestamp}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"💾 נשמר: {filename}")
        return filename


# =====================================================
# Main
# =====================================================

def main():
    """הפונקציה הראשית"""
    print("=" * 60)
    print("🚀 AI News Digest - גרסה משודרגת")
    print("=" * 60 + "\n")
    
    # איסוף חדשות
    articles = fetch_news_from_sources()
    
    if not articles:
        print("⚠️  לא נמצאו כתבות חדשות")
        send_to_telegram("⚠️ לא נמצאו חדשות חדשות ב-24 שעות האחרונות")
        return
    
    # סיכום
    summary = analyze_and_summarize_with_claude(articles)
    
    # שמירת TXT
    output_file = save_output(summary, output_format="txt")
    
    # יצירת PDF (אם אפשרי)
    if PDF_AVAILABLE:
        try:
            pdf_file = create_pdf_digest(summary)
            if pdf_file:
                print(f"📄 PDF נוצר: {pdf_file}")
        except Exception as e:
            print(f"⚠️  לא הצלחתי ליצור PDF: {e}")
    
    # שליחה לטלגרם
    send_to_telegram(summary)
    
    # הדפסה
    print("\n" + "=" * 60)
    print("📋 הסיכום:")
    print("=" * 60)
    print(summary)
    print("\n" + "=" * 60)
    print("✅ תהליך הושלם בהצלחה!")
    print("=" * 60)


if __name__ == "__main__":
    main()


