# 📱 מדריך הוספת טלגרם

## למה זה שימושי?
במקום להיכנס כל יום ל-GitHub ולהוריד את הקובץ, הסיכום יגיע אליך אוטומטית לטלגרם כל בוקר! ☕

---

## 🎯 שלב 1: יצירת בוט בטלגרם

1. פתח את טלגרם ב אפליקציה
2. חפש את **@BotFather** (זה הבוט הרשמי של טלגרם ליצירת בוטים)
3. שלח לו את הפקודה: `/start`
4. שלח לו את הפקודה: `/newbot`
5. תן שם לבוט שלך (למשל: "My AI News Bot")
6. תן username לבוט (חייב להסתיים ב-`bot`, למשל: `my_ai_news_bot`)
7. **BotFather ישלח לך Token** - זה נראה כך:
   ```
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz1234567890
   ```
8. **העתק והשמור את ה-Token הזה!**

---

## 🎯 שלב 2: קבלת Chat ID שלך

כדי שהבוט ידע לאן לשלוח הודעות, צריך את ה-Chat ID שלך:

1. חפש בטלגרם את **@userinfobot**
2. שלח לו `/start`
3. הבוט ישלח לך את ה-ID שלך (מספר כמו `123456789`)
4. **העתק והשמור את המספר הזה!**

---

## 🎯 שלב 3: תיקון הבוט שיוכל לשלוח לך הודעות

חשוב! הבוט צריך להתחיל לדבר איתך לפני שהוא יכול לשלוח הודעות:

1. חפש בטלגרם את הבוט שיצרת (ה-username ש שמת לו)
2. לחץ **"Start"** או שלח לו `/start`
3. זהו! עכשיו הבוט יכול לשלוח לך הודעות

---

## 🎯 שלב 4: הוספת הנתונים ל-GitHub Secrets

חזור ל-Repository שלך ב-GitHub:

1. לך ל-**Settings** → **Secrets and variables** → **Actions**
2. לחץ **"New repository secret"**
3. הוסף את ה-Bot Token:
   - **Name**: `TELEGRAM_BOT_TOKEN`
   - **Value**: ה-Token שקיבלת מ-BotFather
   - לחץ **"Add secret"**
4. לחץ שוב **"New repository secret"**
5. הוסף את ה-Chat ID:
   - **Name**: `TELEGRAM_CHAT_ID`
   - **Value**: ה-ID שקיבלת מ-userinfobot
   - לחץ **"Add secret"**

---

## 🎯 שלב 5: עדכון ה-Workflow

עכשיו צריך לשנות את ה-Workflow שישתמש בגרסת הטלגרם:

1. פתח את הקובץ `.github/workflows/daily-digest.yml`
2. מצא את השורה:
   ```yaml
   run: python news_digest.py
   ```
3. שנה אותה ל:
   ```yaml
   run: python news_digest_telegram.py
   ```
4. הוסף את הנתונים של טלגרם ל-`env`:
   ```yaml
   - name: Run AI News Digest
     env:
       ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
       TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
       TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
     run: |
       python news_digest_telegram.py
   ```

---

## ✅ בדיקה

1. לך ל-**Actions** ב-Repository
2. לחץ על **"AI News Digest - Daily Summary"**
3. לחץ **"Run workflow"** → **"Run workflow"**
4. אחרי כ-30 שניות תקבל את הסיכום ישירות לטלגרם! 🎉

---

## 🛠️ טיפים

### הבוט לא שולח הודעות?
- ודא ששלחת `/start` לבוט
- בדוק שה-Token וה-Chat ID נכונים
- בדוק את ה-Logs ב-GitHub Actions

### רוצה לשלוח לקבוצה?
1. הוסף את הבוט לקבוצה
2. קבל את ה-Chat ID של הקבוצה (באותה צורה עם userinfobot)
3. שים אותו ב-TELEGRAM_CHAT_ID

### רוצה תמונות וגרפים?
אפשר לשדרג את הקוד שישלח גם תמונות, אבל זה יותר מתקדם.

---

## 💡 למה זה עובד?

1. **GitHub Actions** מריץ את הקוד שלך בענן
2. הקוד **אוסף חדשות** מהאינטרנט
3. **Claude** מסכם אותן
4. **Telegram API** שולח את הסיכום ישירות לנייד שלך

הכל אוטומטי, הכל בחינם! 🚀
