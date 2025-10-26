Создай бота у @BotFather → скопируй токен.
В этой же папке:
echo "BOT_TOKEN=12345:AA..." > .env
Локальный запуск: python bot.py
Деплой:
flyctl launch --copy-config -c fly.toml --now
Подключи Telegram Stars: @BotFather → Bot Settings → Payments → Telegram Stars.
Публикуй реф-ссылку в чатах (список из 50 штук уже в bot.py комментарии).
---------------- 9. Как включить монетизацию ----------------
Когда в канале-логе 1 000+ подписчиков – @BotFather → Monetization → Enable.
Рекламные посты приходят автоматически, доход 50/50.
Премиум-кнопка: просто добавь в клавиатуру кнопку «Купить Premium за 49 ⭐» со ссылкой https://t.me/BotName?startchannel=... – Telegram сам покажет окно оплаты Stars.
Готово! Скопируй файлы, запусти – бот уже приносит первые баллы и рефералов.