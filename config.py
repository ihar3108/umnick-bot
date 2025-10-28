import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN   = os.getenv("BOT_TOKEN")          # ← задай в .env
CHANNEL_ID  = os.getenv("CHANNEL_ID", "@umnick_log")   # канал для логов
REF_BONUS   = (20, 10)                        # (приглашённый, пригласивший)
TON_RATE_URL= "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=rub"