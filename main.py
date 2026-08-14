import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

--- GÜVENLİK: Token Server Dashboard'undan (Environment Variable) Çekilir ---
TELEGRAM_TOKEN = os.getenv"8881988772:AAHFeRBjhArmrmMT33Jy-1y-w9YpAl8lR_o"

Log Ayarları
logging.basicConfig(
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
level=logging.INFO
)
logger = logging.getLogger(name)

--- DİL SÖZLÜĞÜ (TR / RU) ---
TEXTS = {
"tr": {
"welcome": "👑 Game of Viyana'ya Hoş Geldiniz, {name}!\n\nLütfen yapmak istediğiniz işlemi seçin:",
"btn_chars": "📜 Karakter Listesi",
"btn_status": "🏰 Krallık Durumu",
"btn_lang": "🌐 Dil Değiştir / Язык",
"btn_back": "🔙 Ana Menü",
"btn_back_chars": "🔙 Karakter Listesine Dön",
"char_select": "🎭 Karakter Listesi:\nDetayını görmek istediğiniz karakteri seçin:",
"status_text": "🏰 Viyana Krallığı Durumu:\n\n• Sınır Güvenliği: Yüksek\n• Ekonomi: Kararlı\n• Aktif Karakter Sayısı: 20",
"lang_select": "🌐 Lütfen bir dil seçin / Пожалуйста, выберите язык:",
"title": "Unvan",
"desc": "Açıklama"
},
"ru": {
"welcome": "👑 Добро пожаловать в Game of Viyana, {name}!\n\nПожалуйста, выберите действие:",
"btn_chars": "📜 Список персонажей",
"btn_status": "🏰 Состояние королевства",
"btn_lang": "🌐 Dil Değiştir / Язык",
"btn_back": "🔙 Главное меню",
"btn_back_chars": "🔙 Назад к списку",
"char_select": "🎭 Список персонажей:\nВыберите персонажа для просмотра деталей:",
"status_text": "🏰 Состояние Королевства Вена:\n\n• Безопасность границ: Высокая\n• Экономика: Стабильная\n• Активных персонажей: 20",
"lang_select": "🌐 Пожалуйста, выберите язык / Lütfen bir dil seçin:",
"title": "Титул",
"desc": "Описание"
}
}

--- ÇOK DİLLİ KARAKTER VERİTABANI ---
CHARACTERS = {
"1": {
"tr": {"name": "Anastasia", "title": "Saray Hanımefendisi", "desc": "Saray içi diplomatik güce sahip stratejist."},
"ru": {"name": "Анастасия", "title": "Придворная дама", "desc": "Стратег с дипломатическим влиянием при дворе."}
},
"2": {
"tr": {"name": "Vasya", "title": "Karakol Muhafızı", "desc": "Sınır güvenlik uzmanı ve muhafız birliği lideri."},
"ru": {"name": "Вася", "title": "Страж аванпоста", "desc": "Эксперт по пограничной безопасности и лидер стражи."}
},
"3": {
"tr": {"name": "Nex", "title": "Siber Operatör", "desc": "Gölge operasyonlar ve taktik istihbarat sorumlusu."},
"ru": {"name": "Некс", "title": "Кибероператор", "desc": "Ответственный за теневые операции и тактическую разведку."}
},
"4": {
"tr": {"name": "Narin", "title": "Zeka ve Taktik Uzmanı", "desc": "Gizli bilgi ağı yöneticisi."},
"ru": {"name": "Нарин", "title": "Тактический эксперт", "desc": "Руководитель секретной информационной сети."}
},
"16": {
"tr": {"name": "Ehed", "title": "Hükümdar / Lider", "desc": "Game of Viyana evreninin mutlak lideri ve stratejisti."},
"ru": {"name": "Эхед", "title": "Правитель / Лидер", "desc": "Абсолютный лидер и стратег вселенной Game of Viyana."}
}
}

Kullanıcı Dilini Getir (Varsayılan: Türkçe)
def get_user_lang(context: ContextTypes.DEFAULT_TYPE) -> str:
return context.user_data.get("lang", "tr")

/start Komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
lang = get_user_lang(context)
txt = TEXTS[lang]
user = update.effective_user

text = txt["welcome"].format(name=user.first_name)

keyboard = [
[InlineKeyboardButton(txt["btn_chars"], callback_data="char_list")],
[InlineKeyboardButton(txt["btn_status"], callback_data="kingdom_status")],
[InlineKeyboardButton(txt["btn_lang"], callback_data="change_lang")]
]
reply_markup = InlineKeyboardMarkup(keyboard)

if update.message:
await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)
elif update.callback_query:
await update.callback_query.message.edit_text(text, parse_mode="Markdown", reply_markup=reply_markup)

Buton İşlemleri
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
query = update.callback_query
await query.answer()

lang = get_user_lang(context)
txt = TEXTS[lang]

# Dil Seçim Menüsü
if query.data == "change_lang":
keyboard = [
[
InlineKeyboardButton("🇹🇷 Türkçe", callback_data="set_lang_tr"),
InlineKeyboardButton("🇷🇺 Русский", callback_data="set_lang_ru")
 ],
[InlineKeyboardButton(txt["btn_back"], callback_data="main_menu")]
]
reply_markup = InlineKeyboardMarkup(keyboard)
await query.message.edit_text(txt["lang_select"], parse_mode="Markdown", reply_markup=reply_markup)

# Dili Türkçe Yap
elif query.data == "set_lang_tr":
context.user_data["lang"] = "tr"
await start(update, context)

# Dili Rusça Yap
elif query.data == "set_lang_ru":
context.user_data["lang"] = "ru"
await start(update, context)

# Karakter Listesi
elif query.data == "char_list":
keyboard = []
for cid, char_data in CHARACTERS.items():
char = char_data.get(lang, char_data["tr"])
keyboard.append([InlineKeyboardButton(f"{char['name']} ({char['title']})", callback_data=f"char_{cid}")])

keyboard.append([InlineKeyboardButton(txt["btn_back"], callback_data="main_menu")])
reply_markup = InlineKeyboardMarkup(keyboard)

await query.message.edit_text(txt["char_select"], parse_mode="Markdown", reply_markup=reply_markup)

# Karakter Detayı
elif query.data.startswith("char_"):
char_id = query.data.split("_")[1]
char_data = CHARACTERS.get(char_id)

if char_data:
char = char_data.get(lang, char_data["tr"])
text = f"👤 {char['name']}\n🎖 {txt['title']}: {char['title']}\n\n📝 {txt['desc']}: {char['desc']}"
keyboard = [[InlineKeyboardButton(txt["btn_back_chars"], callback_data="char_list")]]
reply_markup = InlineKeyboardMarkup(keyboard)

await query.message.edit_text(text, parse_mode="Markdown", reply_markup=reply_markup)

# Krallık Durumu
elif query.data == "kingdom_status":
keyboard = [[InlineKeyboardButton(txt["btn_back"], callback_data="main_menu")]]
reply_markup = InlineKeyboardMarkup(keyboard)
await query.message.edit_text(txt["status_text"], parse_mode="Markdown", reply_markup=reply_markup)

# Ana Menüye Dön
elif query.data == "main_menu":
await start(update, context)

Botu Çalıştır
def main():
if not TELEGRAM_TOKEN:
logger.error("TELEGRAM_TOKEN bulunamadı! Lütfen sunucu panelinizden Environment Variable ekleyin.")
return

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_click))

print("🚀 Game of Viyana Botu (TR/RU) Çalışıyor...")
app.run_polling()

if name == 'main':
main()

