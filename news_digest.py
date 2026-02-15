#!/usr/bin/env python3
"""
AI News Digest - אוטומציה לסיכום חדשות AI
גרסה: 2.1 (Final) - עם תמיכה מלאה בטלגרם
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import feedparser

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
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"


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
                
        except Exception as e:
            print(f"  ⚠️  שגיאה בקריאת {source_name}: {e}")
            continue
    
    print(f"✅ נמצאו {len(all_articles)} כתבות\n")
    return all_articles


# =====================================================
# חלק 3: סינון וסיכום עם Claude (עברית משופרת)
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
    
    # פרומפט משופר לעברית טבעית יותר
    prompt = f"""אתה עיתונאי טכנולוגיה ישראלי מומחה בתחום הבינה המלאכותית.

קיבלת {len(articles)} כתבות מ-8 מקורות שונים שפורסמו ב-24 שעות האחרונות.

המשימה שלך:
1. קרא את כל הכתבות וזהה את הנושאים החשובים
2. אם כמה מקורות דיווחו על אותו נושא - צלוב את המידע ביניהם
3. סנן החוצה חדשות לא רלוונטיות או משניות
4. כתוב סיכום תמציתי בעברית טבעית ושוטפת (לא תרגום מילולי!)
5. השתמש בסדר מילים ישראלי טבעי (נושא-פועל-מושא)
6. חלק לקטגוריות: מוצרים חדשים | מחקרים | חברות והשקעות | כללי

דרישות כתיבה:
- כתוב במשפטים קצרים וברורים
- השתמש בשפה עיתונאית ישראלית (לא ספרותית)
- דוגמאות טובות: "OpenAI השיקה...", "חוקרים גילו...", "החברה גייסה..."
- דוגמאות רעות: "הושק על ידי OpenAI...", "התגלה כי..."
- מקסימום 500 מילים

הכתבות:
{articles_text}

פורמט הסיכום:
# 📰 סיכום חדשות AI - {datetime.now().strftime('%d/%m/%Y')}

## 🆕 מוצרים ושירותים חדשים
[כאן הסיכום]

## 🔬 מחקר ופיתוח
[כאן הסיכום]

## 💰 חברות והשקעות
[כאן הסיכום]

## 📌 כללי
[כאן הסיכום]

---
**מקורות:** [רשימת המקורות שמהם לקחת מידע]
"""

    try:
        # בדיקה שיש API Key
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            error_msg = "❌ שגיאה: ANTHROPIC_API_KEY לא נמצא"
            print(error_msg)
            return error_msg
        
        # קריאה ישירה ל-API עם requests
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
            error_msg = f"❌ שגיאה מה-API: {response.status_code} - {response.text}"
            print(error_msg)
            return error_msg
        
        result = response.json()
        summary = result['content'][0]['text']
        
        print("✅ סיכום הושלם!\n")
        return summary
        
    except Exception as e:
        error_msg = f"❌ שגיאה בקריאה ל-Claude API: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return f"שגיאה בעיבוד: {str(e)}"


# =====================================================
# חלק 4: שליחה לטלגרם
# =====================================================

def send_to_telegram(message: str) -> bool:
    """
    שולח הודעה לטלגרם
    """
    TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️  טלגרם לא מוגדר (חסרים TELEGRAM_BOT_TOKEN או TELEGRAM_CHAT_ID)")
        return False
    
    print(f"📱 שולח הודעה לטלגרם (Chat ID: {TELEGRAM_CHAT_ID[:5]}...)...")
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    # טלגרם מוגבל ל-4096 תווים להודעה
    max_length = 4000
    
    try:
        if len(message) > max_length:
            # חלוקה להודעות מרובות
            parts = [message[i:i+max_length] for i in range(0, len(message), max_length)]
            print(f"📄 ההודעה ארוכה מדי, מחלק ל-{len(parts)} חלקים...")
            
            for i, part in enumerate(parts, 1):
                payload = {
                    "chat_id": TELEGRAM_CHAT_ID,
                    "text": f"📄 חלק {i}/{len(parts)}:\n\n{part}",
                    "parse_mode": "Markdown"
                }
                response = requests.post(url, json=payload, timeout=30)
                
                if response.status_code != 200:
                    print(f"⚠️  שגיאה בשליחת חלק {i}: {response.text}")
                else:
                    print(f"✅ חלק {i}/{len(parts)} נשלח בהצלחה")
        else:
            # הודעה בודדת
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "Markdown"
            }
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                print("✅ הסיכום נשלח לטלגרם בהצלחה! 🎉")
                return True
            else:
                print(f"❌ שגיאה בשליחה לטלגרם: {response.status_code}")
                print(f"   תגובה: {response.text}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ שגיאה בשליחה לטלגרם: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


# =====================================================
# חלק 5: שמירת הפלט
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
        print(f"💾 נשמר: {filename}")
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
        print(f"💾 נשמר: {filename}")
        return filename


# =====================================================
# חלק 6: Main Function
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
        # שליחת הודעה גם אם אין חדשות
        send_to_telegram("⚠️ לא נמצאו חדשות חדשות ב-24 שעות האחרונות")
        return
    
    # שלב 2: ניתוח וסיכום
    summary = analyze_and_summarize_with_claude(articles)
    
    # שלב 3: שמירה
    output_file = save_output(summary, output_format="txt")
    
    # שלב 4: שליחה לטלגרם (החשוב ביותר!)
    send_to_telegram(summary)
    
    # שלב 5: הדפסת הסיכום למסך (לצורך GitHub Actions Logs)
    print("\n" + "=" * 60)
    print("📋 הסיכום:")
    print("=" * 60)
    print(summary)
    print("\n" + "=" * 60)
    print("✅ תהליך הושלם בהצלחה!")
    print("=" * 60)


if __name__ == "__main__":
    main()
