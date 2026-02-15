#!/usr/bin/env python3
"""
הרחבה: שליחה לטלגרם
גרסה מורחבת של news_digest.py שכוללת שליחה אוטומטית לטלגרם
"""

import os
import requests
from news_digest import fetch_news_from_sources, analyze_and_summarize_with_claude

# =====================================================
# הגדרות טלגרם
# =====================================================

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def send_to_telegram(message: str, token: str, chat_id: str) -> bool:
    """
    שולח הודעה לטלגרם
    
    Args:
        message: הטקסט לשליחה
        token: Bot Token מ-BotFather
        chat_id: מזהה הצ'אט (החשבון שלך)
    
    Returns:
        True אם ההודעה נשלחה בהצלחה
    """
    if not token or not chat_id:
        print("❌ חסרים נתוני טלגרם (TELEGRAM_BOT_TOKEN או TELEGRAM_CHAT_ID)")
        return False
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # מחלק הודעות ארוכות (טלגרם מוגבל ל-4096 תווים)
    max_length = 4000
    if len(message) > max_length:
        parts = [message[i:i+max_length] for i in range(0, len(message), max_length)]
        for i, part in enumerate(parts, 1):
            payload = {
                "chat_id": chat_id,
                "text": f"📄 חלק {i}/{len(parts)}:\n\n{part}",
                "parse_mode": "Markdown"
            }
            response = requests.post(url, json=payload)
            if response.status_code != 200:
                print(f"⚠️  שגיאה בשליחת חלק {i}: {response.text}")
                return False
    else:
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"❌ שגיאה בשליחה לטלגרם: {response.text}")
            return False
    
    print("✅ הסיכום נשלח לטלגרם בהצלחה!")
    return True


def main():
    """
    Main function עם שליחה לטלגרם
    """
    print("🚀 AI News Digest + Telegram - מתחיל...")
    
    # שלב 1: איסוף חדשות
    articles = fetch_news_from_sources()
    
    if not articles:
        message = "⚠️ לא נמצאו חדשות חדשות היום"
        send_to_telegram(message, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        return
    
    # שלב 2: סיכום
    summary = analyze_and_summarize_with_claude(articles)
    
    # שלב 3: שליחה לטלגרם
    send_to_telegram(summary, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
    
    print("✅ התהליך הושלם!")


if __name__ == "__main__":
    main()
