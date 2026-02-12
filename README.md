# 🤖 AI News Digest - סיכום חדשות AI אוטומטי

> **מערכת חכמה שאוספת, מסננת ומסכמת עבורך את כל חדשות ה-AI החשובות - כל בוקר ישירות אליך**

---

## 🎯 מה זה עושה?

כל בוקר בשעה שתבחר, המערכת:
1. ✅ סורקת 8 אתרי חדשות מובילים בתחום ה-AI
2. ✅ קוראת עשרות כתבות ומסננת את המיותר
3. ✅ מסכמת את הכי מעניין לסיכום של 2-3 דקות קריאה
4. ✅ שולחת אליך ישירות (טלגרם / WhatsApp / PDF / אימייל)

**כל זה אוטומטי, בחינם, ובלי שצריך להפעיל משהו!**

---

## 🌟 יכולות

- 📰 **8 מקורות חדשות** - TechCrunch, VentureBeat, MIT Tech Review, ועוד
- 🤖 **סיכום חכם** - Claude AI קורא הכל ומסנן רק מה שחשוב
- ⏰ **אוטומציה מלאה** - רץ בענן 24/7 בלי שצריך לעשות כלום
- 📱 **משלוח גמיש** - טלגרם, WhatsApp, PDF, או קובץ טקסט
- 🎨 **התאמה אישית** - שנה את המקורות, השעות, והפורמט
- 💰 **חינמי לחלוטין** - GitHub Actions + Claude API Free Tier

---

## 🚀 התקנה מהירה (10 דקות)

### דרישות מקדימות:
1. חשבון GitHub (חינמי)
2. API Key של Claude (חינמי עד $5/חודש)

### צעדים:
1. **קבל API Key** מ-https://console.anthropic.com/
2. **Fork את ה-Repository הזה** (או צור חדש והעתק את הקבצים)
3. **הוסף Secret** ב-Settings → Secrets:
   - Name: `ANTHROPIC_API_KEY`
   - Value: ה-API Key שלך
4. **הפעל** ב-Actions → Run workflow
5. **תיהנה** מהסיכום! 🎉

📚 **מדריך מפורט צעד-אחר-צעד**: ראה [SETUP_GUIDE.md](SETUP_GUIDE.md)

---

## 📦 מה יש בפרויקט?

```
📁 ai-news-digest/
├── 📄 news_digest.py              # הסקריפט הראשי
├── 📄 news_digest_telegram.py     # גרסה עם טלגרם
├── 📄 news_digest_pdf.py          # גרסה עם PDF מעוצב
├── 📄 requirements.txt            # תלויות Python
├── 📁 .github/workflows/
│   └── 📄 daily-digest.yml        # אוטומציה של GitHub
├── 📄 SETUP_GUIDE.md              # מדריך התקנה מפורט
├── 📄 TELEGRAM_SETUP.md           # מדריך טלגרם
└── 📄 WHATSAPP_SETUP.md           # מדריך WhatsApp
```

---

## 🎨 דוגמאות שימוש

### שימוש בסיסי - קובץ טקסט:
```bash
python news_digest.py
# → יוצר קובץ: ai_news_digest_20240213_080000.txt
```

### שליחה לטלגרם:
```bash
python news_digest_telegram.py
# → שולח ישירות לטלגרם שלך
```

### יצירת PDF מעוצב:
```bash
python news_digest_pdf.py
# → יוצר: ai_news_digest_20240213_080000.pdf
```

---

## ⚙️ התאמה אישית

### שינוי רשימת האתרים

ערוך את `NEWS_SOURCES` ב-`news_digest.py`:

```python
NEWS_SOURCES = {
    "שם המקור": "כתובת RSS Feed",
    "Hacker News AI": "https://hnrss.org/newest?q=AI",
    # הוסף כמה שתרצה!
}
```

### שינוי השעה

ערוך את `.github/workflows/daily-digest.yml`:

```yaml
schedule:
  - cron: '0 8 * * *'  # 08:00 UTC = 10:00 בישראל (חורף)
```

חשב UTC:
- 06:00 UTC = 08:00 ישראל (חורף)
- 18:00 UTC = 20:00 ישראל (חורף)

### שינוי מסגרת הזמן

ערוך ב-`news_digest.py`:
```python
HOURS_BACK = 24  # שנה ל-48 לחדשות מיומיים
```

---

## 📊 מה כלול בסיכום?

הסיכום מחולק לקטגוריות:

1. **🆕 מוצרים ושירותים חדשים**
   - השקות, פיצ'רים חדשים, כלים

2. **🔬 מחקר ופיתוח**
   - מאמרים חדשים, breakthrough-ים, טכנולוגיות

3. **💰 השקעות וחברות**
   - גיוסי הון, מיזוגים, סגירות

4. **📌 אחר**
   - רגולציה, ויכוחים, טרנדים

---

## 💰 עלויות

| שירות | עלות חודשית |
|-------|-------------|
| **GitHub Actions** | **חינם** (2000 דקות) |
| **Claude API** | **$0.30-0.90** (~$0.02/יום) |
| **טלגרם Bot** | **חינם לחלוטין** |
| **WhatsApp (Twilio)** | **$15 חינם** (3000 הודעות) |
| **סה"כ** | **כמעט חינם!** |

---

## 🛠️ שדרוגים מתקדמים

רוצה לשדרג? יש לך אפשרויות:

### 1. שליחה לאימייל
```bash
pip install sendgrid
# הוסף SendGrid API Key
```

### 2. שמירה ב-Google Drive
```bash
pip install google-api-python-client
# הוסף Google Service Account
```

### 3. סינון לפי נושאים
```python
TOPICS_FILTER = ["GPT-4", "Claude", "Computer Vision"]
# Claude יסנן רק כתבות על הנושאים האלה
```

### 4. תרגום לעברית
```python
# הוסף בקשה ל-Claude לתרגם הכל לעברית
```

### 5. גרפים וסטטיסטיקות
```python
# הוסף matplotlib לייצר גרף של טרנדים
```

---

## 🔧 פתרון בעיות

### ❌ "ANTHROPIC_API_KEY not found"
→ ודא שהוספת את ה-Secret ב-GitHub

### ❌ "No articles found"
→ הגדל את `HOURS_BACK` ל-48 או בדוק את ה-RSS Feeds

### ❌ "Rate limit exceeded"
→ אתה מריץ יותר מדי פעמים, חכה קצת

### ❌ הבוט לא שולח לטלגרם
→ שלחת `/start` לבוט? בדוק את ה-Token וה-Chat ID

📚 **עוד עזרה**: פתח Issue ב-GitHub או בדוק את הלוגים ב-Actions

---

## 🤝 תרומה לפרויקט

רוצה לשפר? מוזמן!

1. Fork את הפרויקט
2. צור Branch: `git checkout -b feature/amazing-feature`
3. Commit: `git commit -m 'Add amazing feature'`
4. Push: `git push origin feature/amazing-feature`
5. פתח Pull Request

---

## 📜 רישיון

MIT License - עשה עם זה מה שבא לך!

---

## 🙏 תודות

- **Claude (Anthropic)** - על ה-AI המדהים
- **GitHub** - על Actions החינמיים
- **כל מקורות החדשות** - על המידע האיכותי

---

## 📞 יצירת קשר

- 🐛 **באג?** → פתח Issue
- 💡 **רעיון?** → פתח Discussion
- ⭐ **אהבת?** → תן כוכב לפרויקט!

---

<div align="center">

**עשוי בישראל 🇮🇱 עם ❤️ ו-AI**

[⭐ Star](https://github.com/YOUR_USERNAME/ai-news-digest) | [🐛 Report Bug](https://github.com/YOUR_USERNAME/ai-news-digest/issues) | [💡 Request Feature](https://github.com/YOUR_USERNAME/ai-news-digest/issues)

</div>
