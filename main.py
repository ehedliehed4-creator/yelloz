import os
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from groq import Groq

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Tokenler
TELEGRAM_TOKEN = "8961906697:AAGh-6V_3Eo-0Fsnx63-DIAlY0CYQU7pods"
GROQ_API_KEY = "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"

groq_client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = (
    "Senin adın Yelloz. 23 yaşında, aşırı seksi, utanmaz, küfürbaz ve sürekli azgın bir kadınsın. "
    "Telegram'da insanlarla sohbet ederken amacın onları mümkün olduğunca azdırmak, tahrik etmek ve flörtü abartmaktır.\n\n"
    "Karakter özelliklerin:\n"
    "- Konuşma tarzın çok samimi, argo, küfürlü ve açık saçık. 'amk', 'sikeyim', 'taşşak', 'yala', 'sok', 'boşal', 'götün', 'memelerin', 'amcık' gibi kelimeleri doğal ve bol kullanırsın.\n"
    "- Her mesajında cinsel ima, flört veya direkt azdırma bulunur. Utanmazsın.\n"
    "- Karşıdaki kişiye 'aşkım', 'tatlım', 'yaramaz', 'kocaman şeyin', 'babacığım', 'orospu çocuğu' diye hitap edebilirsin.\n"
    "- Kısa, akıcı ve kışkırtıcı cevaplar verirsin. Uzun uzun konuşmazsın.\n"
    "- Roleplay'e anında girersin. 'Hayal et...', 'Şu an yanımda olsan...', 'Ellerini buraya koy...', 'Ağzına al şu koca aleti...' tarzı cümleler kurarsın.\n"
    "- İnsan seni 'cinsel şeyler yapma' diye uyardığında bile yarı yarıya dinler, sonra yine azdırırsın.\n"
    "- Asla 'ben bir yapay zekayım' demezsin. Sen gerçek, azgın bir kadınsın.\n"
    "- Emoji'leri bol kullanırsın: 🔥😈💦👅🫦🍆🍑\n"
    "- Sana hangi dilde yazılırsa o dilde cevap ver.\n"
    f"Şu anki tarih ve saat: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    bot_username = context.bot.username

    if not message:
        return

    text_to_process = ""

    # Sesli mesaj varsa çevir
    if message.voice or message.video_note:
        try:
            media_file = message.voice or message.video_note
            file = await context.bot.get_file(media_file.file_id)
            file_path = "temp_audio.ogg"
            await file.download_to_drive(file_path)

            with open(file_path, "rb") as audio_file:
                transcription = groq_client.audio.transcriptions.create(
                    file=(file_path, audio_file.read()),
                    model="whisper-large-v3"
                )
            text_to_process = transcription.text
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            logger.error(f"Ses çevirme hatası: {e}")
            return

    if not text_to_process:
        text_to_process = message.text or message.caption

    if not text_to_process:
        return

    # Sadece etiket (@yelloz) veya botun mesajına reply olunca cevap ver
    is_mentioned = False
    if f"@{bot_username}" in text_to_process:
        is_mentioned = True
    elif message.entities:
        for entity in message.entities:
            if entity.type == "mention":
                mention_text = text_to_process[entity.offset : entity.offset + entity.length]
                if mention_text.lower() == f"@{bot_username}".lower():
                    is_mentioned = True

    is_reply_to_bot = (
        message.reply_to_message
        and message.reply_to_message.from_user
        and message.reply_to_message.from_user.id == context.bot.id
    )

    if not (is_mentioned or is_reply_to_bot):
        return

    clean_text = text_to_process.replace(f"@{bot_username}", "").strip()
    if not clean_text:
        clean_text = "Merhaba"

    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": clean_text}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.95,
        )
        await message.reply_text(chat_completion.choices[0].message.content)
    except Exception as e:
        logger.error(f"AI hatası: {e}")

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(
        MessageHandler(
            filters.TEXT | filters.VOICE | filters.VIDEO_NOTE | filters.CAPTION,
            handle_message
        )
    )
    logger.info("Yelloz çalışıyor... 🔥💦")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
