# 🚀 דוגמאות מתקדמות והתאמות

מדריך זה מיועד למי שרוצה להרחיב ולהתאים את המערכת לצרכים ספציפיים.

---

## 📝 דוגמה 1: סינון לפי נושאים ספציפיים

רוצה רק חדשות על GPT, LLMs, או Computer Vision?

```python
# הוסף את הקוד הזה ב-news_digest.py

TOPICS_OF_INTEREST = [
    "GPT",
    "Large Language Models",
    "Computer Vision", 
    "Anthropic",
    "Claude",
    "ChatGPT",
    "Stable Diffusion"
]

def filter_by_topics(articles: List[Dict]) -> List[Dict]:
    """מסנן כתבות לפי נושאים מעניינים"""
    filtered = []
    
    for article in articles:
        title_lower = article['title'].lower()
        summary_lower = article['summary'].lower()
        
        for topic in TOPICS_OF_INTEREST:
            if topic.lower() in title_lower or topic.lower() in summary_lower:
                filtered.append(article)
                break
    
    return filtered

# בתוך main(), אחרי fetch_news_from_sources:
articles = filter_by_topics(articles)
```

---

## 📊 דוגמה 2: הוספת סטטיסטיקות וגרפים

```python
from collections import Counter
import matplotlib.pyplot as plt

def generate_statistics(articles: List[Dict]) -> str:
    """יוצר סטטיסטיקות על החדשות"""
    
    # ספירת כתבות לפי מקור
    sources = Counter([art['source'] for art in articles])
    
    # מציאת מילות מפתח נפוצות
    all_words = []
    for art in articles:
        words = art['title'].split() + art['summary'].split()
        all_words.extend([w.lower() for w in words if len(w) > 4])
    
    common_words = Counter(all_words).most_common(10)
    
    stats = f"""
📊 **סטטיסטיקות היום:**
- סה"כ כתבות: {len(articles)}
- מקורות: {len(sources)}
- המקור המוביל: {sources.most_common(1)[0][0]} ({sources.most_common(1)[0][1]} כתבות)

🔥 **מילות מפתח חמות:**
{chr(10).join([f'  - {word}: {count} פעמים' for word, count in common_words[:5]])}
    """
    
    return stats

# הוסף לסיכום:
stats = generate_statistics(articles)
summary = summary + "\n\n" + stats
```

---

## 🌐 דוגמה 3: תרגום אוטומטי לעברית

```python
def translate_to_hebrew(summary: str) -> str:
    """מתרגם את הסיכום לעברית באמצעות Claude"""
    
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=4000,
        messages=[{
            "role": "user",
            "content": f"""תרגם את הטקסט הבא לעברית בצורה טבעית ושוטפת:

{summary}

דרישות:
- תרגום איכותי ולא מילולי
- שמור על המבנה והפורמט
- התאם ביטויים טכניים לעברית מקצועית
"""
        }]
    )
    
    return message.content[0].text

# שימוש:
summary = analyze_and_summarize_with_claude(articles)
summary_hebrew = translate_to_hebrew(summary)
```

---

## 📧 דוגמה 4: שליחה לאימייל (Gmail)

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject: str, body: str, to_email: str):
    """שולח אימייל דרך Gmail"""
    
    from_email = os.environ.get("GMAIL_ADDRESS")
    password = os.environ.get("GMAIL_APP_PASSWORD")  # לא הסיסמה הרגילה!
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
        print("✅ אימייל נשלח בהצלחה!")
        return True
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        return False

# שימוש:
send_email(
    subject="📰 AI News Digest - " + datetime.now().strftime('%d/%m/%Y'),
    body=summary,
    to_email="your-email@gmail.com"
)
```

**הערה**: צריך App Password מ-Google, לא הסיסמה הרגילה!
1. לך ל: https://myaccount.google.com/apppasswords
2. צור App Password חדש
3. הוסף כ-Secret: `GMAIL_APP_PASSWORD`

---

## 💾 דוגמה 5: שמירה ב-Google Drive

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

```python
from googleapiclient.discovery import build
from google.oauth2 import service_account

def upload_to_drive(filename: str, folder_id: str = None):
    """מעלה קובץ ל-Google Drive"""
    
    # טען את ה-credentials מ-Secret
    creds_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT")
    creds = service_account.Credentials.from_service_account_info(
        json.loads(creds_json)
    )
    
    service = build('drive', 'v3', credentials=creds)
    
    file_metadata = {
        'name': filename,
        'parents': [folder_id] if folder_id else []
    }
    
    media = MediaFileUpload(filename, resumable=True)
    
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    
    print(f"✅ הועלה ל-Drive: {file.get('id')}")
    return file.get('id')
```

---

## 🔔 דוגמה 6: התראות Slack

```python
import requests

def send_to_slack(message: str, webhook_url: str):
    """שולח הודעה ל-Slack"""
    
    payload = {
        "text": message,
        "username": "AI News Bot",
        "icon_emoji": ":newspaper:"
    }
    
    response = requests.post(webhook_url, json=payload)
    
    if response.status_code == 200:
        print("✅ נשלח ל-Slack!")
        return True
    else:
        print(f"❌ שגיאה: {response.text}")
        return False

# צור Slack Webhook:
# https://api.slack.com/messaging/webhooks
# הוסף כ-Secret: SLACK_WEBHOOK_URL
```

---

## 🎯 דוגמה 7: סינון חכם יותר עם Sentiment Analysis

```python
from textblob import TextBlob

def analyze_sentiment(text: str) -> float:
    """מחזיר ציון רגש (-1 = שלילי, +1 = חיובי)"""
    blob = TextBlob(text)
    return blob.sentiment.polarity

def filter_important_news(articles: List[Dict]) -> List[Dict]:
    """סינון מתקדם - רק חדשות חשובות"""
    important = []
    
    for article in articles:
        # חדשות עם "breakthrough", "launch", "release" וכו'
        important_keywords = [
            'breakthrough', 'launch', 'release', 'announce',
            'new', 'first', 'major', 'significant'
        ]
        
        title_lower = article['title'].lower()
        
        # בדוק אם יש מילת מפתח חשובה
        has_keyword = any(kw in title_lower for kw in important_keywords)
        
        # בדוק sentiment (חדשות חיוביות בדרך כלל יותר מעניינות)
        sentiment = analyze_sentiment(article['title'])
        
        if has_keyword or sentiment > 0.2:
            article['importance_score'] = sentiment + (1 if has_keyword else 0)
            important.append(article)
    
    # מיון לפי חשיבות
    important.sort(key=lambda x: x.get('importance_score', 0), reverse=True)
    
    return important[:10]  # רק 10 הכי חשובות
```

---

## 📱 דוגמה 8: Discord Webhook

```python
import requests

def send_to_discord(message: str, webhook_url: str):
    """שולח הודעה ל-Discord"""
    
    # Discord מוגבל ל-2000 תווים
    max_length = 1900
    
    if len(message) > max_length:
        # חלק להודעות
        parts = [message[i:i+max_length] 
                for i in range(0, len(message), max_length)]
        
        for i, part in enumerate(parts, 1):
            payload = {
                "content": f"**📰 AI News Digest - חלק {i}/{len(parts)}**\n{part}",
                "username": "AI News Bot"
            }
            requests.post(webhook_url, json=payload)
    else:
        payload = {
            "content": message,
            "username": "AI News Bot",
            "avatar_url": "https://example.com/bot-avatar.png"
        }
        response = requests.post(webhook_url, json=payload)
        
        if response.status_code == 204:
            print("✅ נשלח ל-Discord!")
        else:
            print(f"❌ שגיאה: {response.text}")

# צור Discord Webhook:
# Settings → Integrations → Webhooks → New Webhook
```

---

## 🗂️ דוגמה 9: ארכיון חודשי אוטומטי

```python
import os
from datetime import datetime

def create_monthly_archive():
    """יוצר ארכיון של כל הסיכומים מהחודש"""
    
    current_month = datetime.now().strftime('%Y_%m')
    archive_dir = f"archives/{current_month}"
    
    os.makedirs(archive_dir, exist_ok=True)
    
    # מעבר על כל קבצי הסיכום
    for filename in os.listdir('.'):
        if filename.startswith('ai_news_digest_') and filename.endswith('.txt'):
            # העבר לארכיון
            os.rename(filename, f"{archive_dir}/{filename}")
    
    print(f"📁 ארכיון נוצר: {archive_dir}")

# הרץ את זה ב-1 לחודש
# ב-workflow, הוסף:
# if: github.event.schedule == '0 0 1 * *'
```

---

## 🔍 דוגמה 10: חיפוש בארכיון

```python
def search_archive(keyword: str, num_results: int = 5):
    """מחפש מילת מפתח בכל הארכיון"""
    
    results = []
    
    for root, dirs, files in os.walk('archives'):
        for file in files:
            if file.endswith('.txt'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if keyword.lower() in content.lower():
                        # חלץ קונטקסט
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if keyword.lower() in line.lower():
                                context = '\n'.join(lines[max(0,i-2):i+3])
                                results.append({
                                    'file': file,
                                    'context': context
                                })
                                break
    
    return results[:num_results]

# שימוש:
results = search_archive("GPT-4")
for r in results:
    print(f"📄 {r['file']}")
    print(r['context'])
    print("---")
```

---

## 🎨 דוגמה 11: פורמט HTML מעוצב

```python
def create_html_digest(summary: str, articles: List[Dict]) -> str:
    """יוצר HTML מעוצב"""
    
    html = f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="he">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 40px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }}
            .container {{
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }}
            h1 {{
                color: #667eea;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
            }}
            .article {{
                border-left: 4px solid #764ba2;
                padding-left: 15px;
                margin: 20px 0;
            }}
            .source {{
                color: #666;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📰 AI News Digest</h1>
            <p><strong>תאריך:</strong> {datetime.now().strftime('%d/%m/%Y')}</p>
            
            <div class="summary">
                <h2>סיכום</h2>
                {summary.replace('\n', '<br>')}
            </div>
            
            <h2>כתבות מקוריות</h2>
            {"".join([f'''
            <div class="article">
                <h3>{art['title']}</h3>
                <p class="source">מקור: {art['source']}</p>
                <a href="{art['link']}">קרא עוד →</a>
            </div>
            ''' for art in articles[:10]])}
        </div>
    </body>
    </html>
    """
    
    return html

# שמור כ-HTML
with open('digest.html', 'w', encoding='utf-8') as f:
    f.write(create_html_digest(summary, articles))
```

---

## 🧪 דוגמה 12: בדיקות A/B על הפרומפט

```python
PROMPTS = {
    "concise": "צור סיכום קצר ותמציתי של 200 מילים",
    "detailed": "צור סיכום מפורט עם ניתוח עמוק",
    "bullet_points": "צור רשימת bullet points של העיקרים",
}

def test_prompts(articles: List[Dict]):
    """בודק איזה פרומפט נותן תוצאות יותר טובות"""
    
    results = {}
    
    for name, prompt_style in PROMPTS.items():
        print(f"🧪 בודק פרומפט: {name}")
        
        # הרץ את הסיכום
        summary = analyze_and_summarize_with_claude(
            articles, 
            custom_prompt=prompt_style
        )
        
        results[name] = {
            'length': len(summary),
            'summary': summary
        }
    
    return results
```

---

## 💡 טיפים נוספים

### מהירות:
- השתמש ב-`asyncio` לקריאות מקבילות מ-RSS
- שמור cache של כתבות שכבר עובדו

### איכות:
- הוסף אימות שכתבות באמת רלוונטיות ל-AI
- התאם את הפרומפט לפי המטרה שלך

### אמינות:
- הוסף retry logic לקריאות API
- שמור backup של הארכיון

---

בהצלחה! 🚀
