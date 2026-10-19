import os
import telebot
from yt_dlp import YoutubeDL

# @BotFather bergan tokeningizni mana shu tirnoq (' ') ichiga yozing:
TOKEN = '8806292202:AAFEJRz0Y5Q6T10OUDK7efq6uRB2-1O18gQ'

try:
    bot = telebot.TeleBot(TOKEN)
    print("Bot ulanishga harakat qilmoqda...")
except Exception as e:
    print(f"Token xato: {e}")

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(
        message, 
        "Salom! 👋\n\nMenga video havola (link) yuboring, men sizga videoni yuklab beraman! 🎵🎬",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: message.text and ("http://" in message.text or "https://" in message.text))
def handle_link(message):
    msg = bot.reply_to(message, "⏳ Yuklanmoqda, kuting...")
    url = message.text.strip()
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'video_{message.chat.id}.%(ext)s',
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_filename = ydl.prepare_filename(info)
            
        with open(video_filename, 'rb') as video:
            bot.send_video(message.chat.id, video, caption="🎬 Yuklangan video\n\n@skachatchi777_bot")
            
        if os.path.exists(video_filename): 
            os.remove(video_filename)
            
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ Yuklashda xatolik yuz berdi: {e}", message.chat.id, msg.message_id)

@bot.message_handler(content_types=['video'])
def handle_video_file(message):
    bot.reply_to(message, "✅ Video qabul qilindi! (Hozircha faqat havolalar orqali yuklash ishlaydi, iltimos video havolasini yuboring).")

print("Bot ishga tushdi va doimiy ishlayapti...")
try:
    bot.polling(none_stop=True)
except Exception as e:
    print(f"Xatolik yuz berdi: {e}")
