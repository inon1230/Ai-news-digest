#!/usr/bin/env python3
"""
AI News Digest - אוטומציה לסיכום חדשות AI
גרסה: 1.1 (Fixed)
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import feedparser
from anthropic import Anthropic

# =====================================================
# חלק 1: הגדרות וקונפיגורציה
# =====================================================

# רשימת אתרי החדשות (RSS Feeds)
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

# הגדרות זמן - כמה שעות אחורה לחפש חדשות
HOURS_BACK = 24

# הגדרות Claude API
CLAUDE_MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 4000


# =====================================================
# חלק 2: איסוף חדשות מ-RSS
# =====================================================

def fetch_news_from_sources(hours_back: int = HOURS_BACK) -> List[Dict]:
    """
    אוסף חדשות מכל המקורות
    """
    print(f"🔍 מחפש חדשות מ-{hours_back} שעות אחורה...")
    
    all_articles = []
    cutoff_time = datetime.now() - timedelta(hours=hours_back)
    
    for source_name, feed_url in NEWS_SOURCES.items():
        try:
            print(f"  📰 קורא: {source_name}")
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries[:15]:  # מגביל ל-15 כתבות אחרונות מכל מקור
                # בודק אם הכתבה חדשה מספיק
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
                
        except Exception as e:
            print(f"  ⚠️  שגיאה בקריאת {source_name}: {e}")
            continue
    
    print(f"✅ נמצאו {len(all_articles)} כתבות\n")
    return all_articles


# =====================================================
# חלק 3: סינון וסיכום עם Claude
# =====================================================

def analyze_and_summarize_with_claude(articles: List[Dict]) -> str:
    """
    שולח את הכתבות ל-Claude לסינון וסיכום
    """
    if not articles:
        return "לא נמצאו חדשות חדשות ב-24 שעות האחרונות."
    
    print(f"🤖 שולח {len(articles)} כתבות ל-Claude לניתוח...")
    
    # בונה את הפרומפט ל-Claude
    articles_text = "\n\n".join([
        f"[{i+1}] {art['source']}\nכותרת: {art['title']}\nתקציר: {art['summary'][:300]}...\nקישור: {art['link']}"
        for i, art in enumerate(articles)
    ])
    
    prompt = f"""אתה עוזר שמתמחה בסיכום חדשות טכנולוגיה בתחום ה-AI.

קיבלת {len(articles)} כתבות מהיממה האחרונה.

המשימה שלך:
1. סנן את הכתבות - השאר רק את אלו שבאמת מעניינות ורלוונטיות (התפתחויות משמעותיות, מוצרים חדשים, מחקרים חשובים)
2. צור סיכום תמציתי בעברית, מקסימום 500 מילים
3. חלק לקטגוריות: מוצרים חדשים, מחקרים, חברות וכסף, אחר
4. כתוב בצורה ישירה וברורה, בלי מלל מיותר

הכתבות:
{articles_text}

פורמט הסיכום:
# 📰 סיכום חדשות AI - {datetime.now().strftime('%d/%m/%Y')}

[הסיכום שלך כאן - תמציתי וממוקד]

---
מקורות: [רשימת המקורות שמהם לקחת]
"""

    try:
        # בדיקה שיש API Key
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            error_msg = "❌ שגיאה: ANTHROPIC_API_KEY לא נמצא"
            print(error_msg)
            return error_msg
        
        # התיקון החשוב: רק api_key, בלי proxies!
        client = Anthropic(api_key=api_key)
        
        message = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        summary = message.content[0].text
        print("✅ סיכום הושלם!\n")
        return summary
        
    except Exception as e:
        error_msg = f"❌ שגיאה בקריאה ל-Claude API: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return f"שגיאה בעיבוד: {str(e)}"


# =====================================================
# חלק 4: שמירת הפלט
# =====================================================

def save_output(summary: str, output_format: str = "txt"):
    """
    שומר את הסיכום בפורמט הרצוי
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if output_format == "txt":
        filename = f"ai_news_digest_{timestamp}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"💾 נשמר בקובץ: {filename}")
        return filename
    
    elif output_format == "json":
        filename = f"ai_news_digest_{timestamp}.json"
        data = {
            "timestamp": timestamp,
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "summary": summary
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 נשמר בקובץ JSON: {filename}")
        return filename


# =====================================================
# חלק 5: Main Function
# =====================================================

def main():
    """
    הפונקציה הראשית שמריצה את כל התהליך
    """
    print("=" * 60)
    print("🚀 AI News Digest - מתחיל לעבוד...")
    print("=" * 60 + "\n")
    
    # שלב 1: איסוף חדשות
    articles = fetch_news_from_sources()
    
    if not articles:
        print("⚠️  לא נמצאו כתבות חדשות")
        return
    
    # שלב 2: ניתוח וסיכום
    summary = analyze_and_summarize_with_claude(articles)
    
    # שלב 3: שמירה
    output_file = save_output(summary, output_format="txt")
    
    # הדפסת הסיכום למסך (לצורך GitHub Actions Logs)
    print("\n" + "=" * 60)
    print("📋 הסיכום:")
    print("=" * 60)
    print(summary)
    print("\n" + "=" * 60)
    print("✅ תהליך הושלם בהצלחה!")
    print("=" * 60)


if __name__ == "__main__":
    main()
