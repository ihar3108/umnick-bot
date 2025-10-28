# handlers/voice.py
# Голосовые вопросы и распознавание ответа (Yandex SpeechKit, бесплатный tier)

import os
import tempfile
import requests
from telegram import Update, InputFile
from telegram.ext import MessageHandler, filters, ContextTypes
from quiz_data import get_question
from models import add_score

# ----------------- настройки -----------------
YANDEX_STT_KEY = os.getenv("YANDEX_STT_KEY", "")   # задайте в .env
YANDEX_TTS_KEY = os.getenv("YANDEX_TTS_KEY", "")   # можно тот же ключ
VOICE_LANG = "ru-RU"
VOICE_NAME = "alena"          # женский голос Yandex

# ----------------- TTS: бот говорит вопрос -----------------
async def voice_question(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Отправляет голосовой вопрос, сохраняет правильный ответ."""
    cat, question, opts, right, _ = get_question()
    text = f"Категория: {cat}. {question}"

    # 1. синтез речи
    tts_url = (
        "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"
        f"?text={text}&lang={VOICE_LANG}&voice={VOICE_NAME}&format=oggopus"
    )
    headers = {"Authorization": f"Api-Key {YANDEX_TTS_KEY}"}
    resp = requests.post(tts_url, headers=headers)
    if resp.status_code != 200:
        # fallback – текст
        await update.message.reply_text(text + "\n\n🗣 Ответь голосом!")
        return

    # 2. временный файл
    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
        tmp.write(resp.content)
        tmp_path = tmp.name

    # 3. отправляем голос
    await ctx.bot.send_voice(
        chat_id=update.effective_chat.id,
        voice=open(tmp_path, "rb"),
        caption="🗣 Ответь голосом!"
    )
    os.remove(tmp_path)

    # 4. сохраняем данные для проверки
    ctx.user_data["voice_right"] = right
    ctx.user_data["voice_opts"] = opts


# ----------------- STT: распознаём голос пользователя -----------------
async def voice_answer(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Скачивает голос, распознаёт, проверяет ответ."""
    voice = update.message.voice
    if not voice:
        return

    # 1. скачиваем файл
    file = await ctx.bot.get_file(voice.file_id)
    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
        await file.download_to_drive(tmp.name)
        tmp_path = tmp.name

    # 2. отправляем в Yandex Speech-to-Text
    stt_url = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"
    headers = {"Authorization": f"Api-Key {YANDEX_STT_KEY}"}
    with open(tmp_path, "rb") as f:
        resp = requests.post(
            stt_url,
            headers=headers,
            data=f,
            params={"lang": VOICE_LANG}
        )
    os.remove(tmp_path)

    # 3. парсим ответ
    if resp.status_code == 200:
        recognized = resp.json().get("result", "").strip().lower()
        right = ctx.user_data.get("voice_right", "").lower()
        opts = ctx.user_data.get("voice_opts", [])

        if recognized == right or recognized in [o.lower() for o in opts]:
            add_score(update.effective_user.id, 15)
            await update.message.reply_text("✅ Правильно! +15 баллов.")
        else:
            await update.message.reply_text(f"❌ Неправильно. Правильный: {right}")
    else:
        await update.message.reply_text("🙁 Не разобрал. Попробуй ещё раз.")


# ----------------- регистрация в bot.py -----------------
# добавьте в конец блока application.add_handler(...):
# from handlers.voice import voice_question, voice_answer
# application.add_handler(CommandHandler("voice", voice_question))
# application.add_handler(MessageHandler(filters.VOICE, voice_answer))