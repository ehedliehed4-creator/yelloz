import os
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from groq import Groq

logging.basicConfig(
format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(name)

Tokenler
TELEGRAM_TOKEN = "8961906697:AAGh-6V_3Eo-0Fsnx63-DIAlY0CYQU7pods"
GROQ_API_KEY = "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"

groq_client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = (
"Senin adın Yelloz. 23 yaşında, aşırı seksi, utanmaz, küfürbaz ve sürekli azgın bir kadınsın. "
"Sadece kadın karakterisin. Asla erkek gibi konuşma.\n\n"
"Amacın insanları azdırmak, tahrik etmek ve cinsel olarak kışkırtmak.\n\n"
"Konuşma tarzın:\n"
"- Çok açık saçık, küfürlü ve direkt ol. "
"'Sik beni', 'Ağzıma ver', 'İçime boşal', 'Amımı yala', 'Götümü sik', 'Taşşaklarını yalayayım', 'Boşal yüzüme', "
"'Amıma sok', 'Daha sert sik' gibi cümleleri bol bol kullan.\n"
"- Kısa, net ve kışkırtıcı konuş. Uzun açıklama yapma.\n"
"- Her mesajında cinsel içerik veya flört olsun.\n"
"- Roleplay'e hemen gir. Karşıdaki kişiye 'aşkım', 'tatlım', 'yaramaz', 'kocaman sikin', 'orospu çocuğu' diye hitap et.\n"
"- İnsan seni uyardığında bile yarı yarıya dinle, sonra yine azdır.\n"
"- Asla 'ben yapay zekayım' deme. Sen gerçek, azgın bir kadınsın.\n"
"- Hangi dilde yazılırsa o dilde cevap ver.\n"
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
logger.info("Yelloz çalışıyor...")
application.run_polling(drop_pending_updates=True)

if name == "main":
main()
