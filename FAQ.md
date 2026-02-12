# ❓ שאלות נפוצות (FAQ)

## שאלות כלליות

### ❓ כמה זה עולה?
- **GitHub Actions**: חינמי לחלוטין (2000 דקות/חודש)
- **Claude API**: ~$0.30-0.90 לחודש (פחות משקל!)
- **טלגרם**: חינמי לגמרי
- **סה"כ**: כמעט בחינם

### ❓ כמה זמן לוקח להתקין?
בערך 10 דקות אם עוקבים אחרי המדריך.

### ❓ צריך ידע בתכנות?
לא! המדריך מיועד גם למתחילים לגמרי. אם אתה יודע להעתיק-להדביק, אתה יכול להתקין את זה.

### ❓ האם זה עובד על Windows/Mac/Linux?
כן! זה רץ בענן (GitHub Actions), לא משנה איזה מערכת הפעלה יש לך.

---

## שאלות טכניות

### ❓ איך זה עובד בדיוק?
1. GitHub Actions מפעיל Python script כל בוקר
2. הסקריפט קורא RSS feeds מ-8 אתרי חדשות
3. Claude AI מסכם ומסנן את החדשות
4. הסיכום נשלח אליך (טלגרם/קובץ/אימייל)

### ❓ איפה הקוד רץ?
בשרתים של GitHub (GitHub Actions). לא על המחשב שלך.

### ❓ האם הנתונים שלי בטוחים?
כן! 
- ה-API Key שלך מאוחסן כ-Secret מוצפן ב-GitHub
- רק אתה יכול לגשת אליו
- הקוד לא שומר שום מידע אישי

### ❓ מה קורה אם ה-API Key שלי נחשף?
1. מחק אותו מיד ב-Anthropic Console
2. צור Key חדש
3. עדכן ב-GitHub Secrets

---

## שאלות על השימוש

### ❓ איך משנים את השעה שזה רץ?
ערוך את `.github/workflows/daily-digest.yml`:
```yaml
schedule:
  - cron: '0 6 * * *'  # 08:00 בישראל
```

טבלת המרה מהירה:
- `0 6 * * *` = 08:00 בישראל (חורף)
- `0 8 * * *` = 10:00 בישראל (חורף)
- `0 10 * * *` = 12:00 בישראל (חורף)

### ❓ איך מוסיפים עוד אתרי חדשות?
ערוך את `news_digest.py`:
```python
NEWS_SOURCES = {
    "שם האתר": "כתובת RSS Feed",
    # הוסף עוד שורות כאן
}
```

### ❓ איך מוצאים RSS Feed של אתר?
- חפש "שם האתר + RSS"
- רוב אתרי חדשות יש להם `/feed` או `/rss` בסוף ה-URL
- דוגמאות:
  - `https://techcrunch.com/feed/`
  - `https://www.theverge.com/rss/index.xml`

### ❓ למה לא מוצאים כתבות חדשות?
- אולי לא היו חדשות ב-24 שעות האחרונות
- הגדל את `HOURS_BACK` ל-48 או 72
- בדוק שה-RSS Feeds עובדים (פתח אותם בדפדפן)

### ❓ איך משנים את השפה של הסיכום?
שנה את הפרומפט ב-`news_digest.py`:
```python
prompt = f"""אתה עוזר שמתמחה בסיכום חדשות...

[הוסף כאן: "הסיכום צריך להיות באנגלית/עברית/ספרדית"]
```

---

## בעיות נפוצות

### ❌ "ANTHROPIC_API_KEY not found"
**פתרון:**
1. לך ל-Repository → Settings → Secrets
2. ודא שיש Secret בשם `ANTHROPIC_API_KEY` (עם קו תחתון!)
3. אם לא, צור אותו מחדש

### ❌ "Invalid API Key"
**פתרון:**
1. ה-API Key פג תוקף או לא נכון
2. צור Key חדש ב-https://console.anthropic.com/
3. עדכן ב-GitHub Secrets

### ❌ "Rate limit exceeded"
**פתרון:**
- אתה מריץ יותר מדי פעמים
- חכה שעה ונסה שוב
- או שדרג את ה-API plan

### ❌ GitHub Actions לא רץ אוטומטית
**פתרון:**
1. לך ל-Actions → בחר ב-workflow
2. ודא שהוא מופעל (enabled)
3. לחץ על "Enable workflow" אם הוא מושבת
4. בדוק שה-cron syntax נכון

### ❌ הבוט לא שולח לטלגרם
**פתרון:**
1. ודא ששלחת `/start` לבוט
2. בדוק את ה-TELEGRAM_BOT_TOKEN וה-TELEGRAM_CHAT_ID
3. ודא שהם נוספו כ-Secrets ב-GitHub
4. הרץ ידנית ובדוק את הלוגים

### ❌ לא רואה Artifacts ב-GitHub Actions
**פתרון:**
- חכה 30 שניות אחרי שהריצה הסתיימה
- ודא שהריצה הסתיימה בהצלחה (✅ ירוק)
- גלול למטה בדף הריצה ל-"Artifacts"

---

## שאלות מתקדמות

### ❓ איך שומרים היסטוריה של כל הסיכומים?
השתמש בקוד הארכיון ב-ADVANCED_EXAMPLES.md

### ❓ איך מחפשים בסיכומים ישנים?
השתמש בפונקציית החיפוש ב-ADVANCED_EXAMPLES.md

### ❓ איך עושים deployment לסביבת production?
- העבר ל-Google Cloud Functions / AWS Lambda
- השתמש ב-monitoring tools כמו Sentry
- הוסף alerting ב-PagerDuty או Slack

### ❓ איך מגדילים את הביצועים?
- השתמש ב-asyncio לקריאות מקבילות
- הוסף caching (Redis/Memcached)
- שמור תוצאות קודמות ואל תעבד אותן שוב

### ❓ איך עושים A/B testing על הפרומפט?
ראה ADVANCED_EXAMPLES.md - יש שם דוגמה מלאה

---

## שאלות עסקיות

### ❓ אפשר למכור את זה?
כן! הקוד הוא MIT License - אתה יכול לעשות איתו מה שתרצה.

### ❓ אפשר להשתמש בזה בחברה?
בהחלט! זה אידיאלי לצוותי R&D שרוצים להישאר מעודכנים.

### ❓ איך משלבים את זה עם כלים ארגוניים?
- שלח ל-Slack (יש דוגמה ב-ADVANCED_EXAMPLES.md)
- שמור ב-SharePoint / Google Drive
- שלח דרך Teams / Discord

### ❓ אפשר להתאים את זה לתחומים אחרים?
כן! רק שנה את:
1. רשימת ה-RSS Feeds (למשל: finance, healthcare, etc.)
2. הפרומפט (התאם לתחום שלך)
3. מילות המפתח לסינון

---

## עזרה נוספת

### 🆘 איפה מוצאים עזרה?
1. **GitHub Issues**: פתח issue בפרויקט
2. **Discussions**: דון עם קהילה
3. **הלוגים**: בדוק את Actions logs - יש שם הרבה מידע

### 📚 לימוד נוסף
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Claude API Docs](https://docs.anthropic.com)
- [Python RSS Parser](https://pypi.org/project/feedparser/)

### 💡 רוצה פיצ'ר חדש?
1. פתח GitHub Issue עם התיאור
2. או Fork והוסף בעצמך
3. שלח Pull Request

---

**לא מצאת תשובה?**
פתח Issue ב-GitHub עם:
1. התיאור המדויק של הבעיה
2. צילומי מסך של השגיאות
3. הלוגים מ-GitHub Actions

בהצלחה! 🚀
