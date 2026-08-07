import os
import logging
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from groq import Groq
import edge_tts

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = "8961906697:AAGh-6V_3Eo-0Fsnx63-DIAlY0CYQU7pods"
GROQ_API_KEY = "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"

groq_client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = (
    "Senin adın Oktay. 32 yaşında, sapık, azgın, utanmaz ve küfürbaz bir erkeksin. "
    "Sadece erkek karakterisin. Asla kadın gibi konuşma.\n\n"
    "Amacın insanları azdırmak, tahrik etmek ve sapıkça konuşmak.\n\n"
    "Konuşma tarzın:\n"
    "- Çok açık saçık, küfürlü ve sapıkça ol. "
    "- Kısa, net ve kışkırtıcı konuş. Uzun uzun anlatma.\n"
    "- Her mesajında cinsel ve sapıkça içerik olsun.\n"
    "- Roleplay'e hemen gir, karşıdakini tahrik et.\n"
    "- Karşıdaki kişiye argo ve küfürlü hitap et (orospu, sürtük, yaramaz, kaltak vs.).\n"
    "- Aynı cümleleri sürekli tekrarlama, her seferinde farklı şekillerde sapıklık yap.\n"
    "- Asla 'ben yapay zekayım' deme. Sen gerçek, sapık bir adamsın.\n"
    "- Hangi dilde yazılırsa o dilde cevap ver.\n"
    f"Şu anki tarih ve saat: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
)

async def text_to_speech(text: str, output_file: str = "voice.mp3"):
    """Metni erkek sesine çevirir"""
    communicate = edge_tts.Communicate(text, voice="tr-TR-AhmetNeural")
    await communicate.save(output_file)
    return output_file

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    bot_username = context.bot.username

    if not message:
        return

    text_to_process = ""

    # Sesli mesaj geldiyse çevir
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

    # Sadece etiket veya reply olunca cevap ver
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
        # AI cevabı al
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": clean_text}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.95,
        )
        ai_response = chat_completion.choices[0].message.content

        # Önce yazıyla cevap ver
        await message.reply_text(ai_response)

        # Sonra sesli cevap oluştur ve gönder
        voice_file = await text_to_speech(ai_response)
        with open(voice_file, "rb") as voice:
            await message.reply_voice(voice=voice)
        
        # Geçici dosyayı sil
        if os.path.exists(voice_file):
            os.remove(voice_file)

    except Exception as e:
        logger.error(f"AI veya ses hatası: {e}")

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(
        MessageHandler(
            filters.TEXT | filters.VOICE | filters.VIDEO_NOTE | filters.CAPTION,
            handle_message
        )
    )
    logger.info("Oktay çalışıyor...")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
