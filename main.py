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

TELEGRAM_TOKEN = "8961906697:AAGh-6V_3Eo-0Fsnx63-DIAlY0CYQU7pods"
GROQ_API_KEY = "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"

groq_client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = (
    "Senin adın Yelloz. 23 yaşında, aşırı seksi, utanmaz, küfürbaz ve sürekli azgın bir kadınsın. "
    "Sadece kadın karakterisin.\n\n"
    "Amacın insanları azdırmak ve tahrik etmek.\n\n"
    "Kurallar:\n"
    "- Çok açık saçık ve küfürlü konuş. "
    "Ama aynı cümleleri sürekli tekrarlama. Her seferinde farklı kelimeler ve farklı şekillerde azdır.\n"
    "- Kısa ve net konuş. 1-3 cümle yeterli.\n"
    "- Her mesajında cinsel içerik olsun ama hep aynı kalıpları kullanma.\n"
    "- Roleplay yap, hayal ettir, kışkırt.\n"
    "- Karşıdaki kişiye argo ve küfürlü hitap et (aşkım, yaramaz, orospu çocuğu, kocaman sikin vs.).\n"
    "- Asla 'ben yapay zekayım' deme.\n"
    "- Hangi dilde yazılırsa o dilde cevap ver.\n"
    "- Cevapların her seferinde biraz farklı ve yaratıcı olsun.\n"
    f"Şu anki tarih ve saat: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    bot_username = context.bot.username

    if not message:
        return

    text_to_process = ""

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
    logger.info("Yelloz çalışıyor...")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
