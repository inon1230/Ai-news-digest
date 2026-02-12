# 📱 מדריך שליחה ל-WhatsApp

## ⚠️ חשוב לדעת

שליחה ל-WhatsApp מורכבת יותר מטלגרם כי:
1. WhatsApp לא נותנת API חינמי (צריך Twilio או שירות אחר)
2. Twilio נותן **טריאל חינמי** אבל מוגבל
3. אפשר רק לשלוח לעצמך (למספר שרשמת)

**המלצה שלי**: התחל עם **טלגרם** - זה הרבה יותר פשוט וחינמי לגמרי!

אבל אם בכל זאת רוצה WhatsApp, הנה המדריך:

---

## 🎯 שלב 1: הרשמה ל-Twilio

1. היכנס ל: https://www.twilio.com/try-twilio
2. הירשם (צריך מספר טלפון לאימות)
3. Twilio ייתן לך **$15 קרדיט חינמי**
4. בדף ה-Console, תקבל:
   - **Account SID** (מזהה חשבון)
   - **Auth Token** (מפתח אימות)
5. **שמור את שניהם!**

---

## 🎯 שלב 2: הגדרת WhatsApp Sandbox

1. בדף ה-Console של Twilio, לך ל-**Messaging** → **Try it out** → **Send a WhatsApp message**
2. תראה מספר כמו: `+1 415 523 8886`
3. תראה קוד כמו: `join [קוד-מיוחד]`
4. **פתח את WhatsApp בטלפון שלך**
5. שלח ל-`+1 415 523 8886` את ההודעה: `join [הקוד]`
6. תקבל הודעה שאתה מחובר! ✅

---

## 🎯 שלב 3: הוספת הנתונים ל-GitHub

1. לך ל-Repository → **Settings** → **Secrets and variables** → **Actions**
2. הוסף 3 Secrets:

   **Secret 1:**
   - Name: `TWILIO_ACCOUNT_SID`
   - Value: ה-Account SID שקיבלת

   **Secret 2:**
   - Name: `TWILIO_AUTH_TOKEN`
   - Value: ה-Auth Token שקיבלת

   **Secret 3:**
   - Name: `WHATSAPP_TO_NUMBER`
   - Value: מספר הטלפון שלך בפורמט: `whatsapp:+972501234567`
   (החלף ל-מספר שלך!)

---

## 🎯 שלב 4: התקנת הספרייה

הוסף את השורה הזו ל-`requirements.txt`:
```
twilio==8.11.0
```

---

## 🎯 שלב 5: הקוד

צור קובץ חדש `news_digest_whatsapp.py`:

```python
#!/usr/bin/env python3
import os
from twilio.rest import Client
from news_digest import fetch_news_from_sources, analyze_and_summarize_with_claude

def send_to_whatsapp(message: str) -> bool:
    """שולח הודעה ל-WhatsApp דרך Twilio"""
    
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    to_number = os.environ.get("WHATSAPP_TO_NUMBER")
    
    if not all([account_sid, auth_token, to_number]):
        print("❌ חסרים נתוני Twilio")
        return False
    
    try:
        client = Client(account_sid, auth_token)
        
        # WhatsApp מוגבל ל-1600 תווים, אז נחלק
        max_length = 1500
        if len(message) > max_length:
            parts = [message[i:i+max_length] 
                    for i in range(0, len(message), max_length)]
            
            for i, part in enumerate(parts, 1):
                msg = client.messages.create(
                    body=f"📄 חלק {i}/{len(parts)}:\n\n{part}",
                    from_='whatsapp:+14155238886',  # מספר Twilio Sandbox
                    to=to_number
                )
                print(f"✅ חלק {i} נשלח: {msg.sid}")
        else:
            msg = client.messages.create(
                body=message,
                from_='whatsapp:+14155238886',
                to=to_number
            )
            print(f"✅ הודעה נשלחה: {msg.sid}")
        
        return True
        
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        return False


def main():
    print("🚀 AI News Digest + WhatsApp - מתחיל...")
    
    # איסוף וסיכום
    articles = fetch_news_from_sources()
    if not articles:
        send_to_whatsapp("⚠️ לא נמצאו חדשות חדשות היום")
        return
    
    summary = analyze_and_summarize_with_claude(articles)
    
    # שליחה ל-WhatsApp
    send_to_whatsapp(summary)
    print("✅ הושלם!")


if __name__ == "__main__":
    main()
```

---

## 🎯 שלב 6: עדכון ה-Workflow

ב-`.github/workflows/daily-digest.yml`, שנה:

```yaml
- name: Run AI News Digest
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
    TWILIO_ACCOUNT_SID: ${{ secrets.TWILIO_ACCOUNT_SID }}
    TWILIO_AUTH_TOKEN: ${{ secrets.TWILIO_AUTH_TOKEN }}
    WHATSAPP_TO_NUMBER: ${{ secrets.WHATSAPP_TO_NUMBER }}
  run: |
    python news_digest_whatsapp.py
```

---

## 💰 עלויות

- **Sandbox (בדיקות)**: חינם לחלוטין!
- **בפרודקשן**: ~$0.005 להודעה (חצי סנט)
- עם $15 קרדיט = **3000 הודעות**
- אם תשלח פעם ביום = **8 שנים של הודעות חינם** 🎉

---

## 🆚 טלגרם vs WhatsApp

| תכונה | טלגרם | WhatsApp |
|-------|--------|----------|
| **עלות** | חינם לגמרי | $15 חינם, אז $0.005/msg |
| **קלות התקנה** | קל מאוד | בינוני |
| **גבולות** | ללא הגבלה | 1600 תווים |
| **המלצה** | ✅ מומלץ למתחילים | רק אם חייבים WhatsApp |

---

## 🛠️ טיפים

### שגיאה: "from number is not a valid WhatsApp number"
- ודא שהשתמשת במספר ה-Sandbox הנכון
- בדוק שעשית את ה-join בצורה נכונה

### רוצה לשדרג לפרודקשן?
צריך:
1. לקנות מספר טלפון ייעודי (דרך Twilio)
2. לעבור אישור של WhatsApp Business API
3. זה כבר יותר מסובך ועולה כסף

### חלופה: WhatsApp Business API בחינם
יש שירותים כמו **Wati.io** ו-**MessageBird** שנותנים WhatsApp בחינם עם הגבלות.

---

בהצלחה! 🚀
