import os

# --- Core project info ---
BOT_NAME = "pricetrack_pro"
SPIDER_MODULES = ["pricetrack_pro.spiders"]
NEWSPIDER_MODULE = "pricetrack_pro.spiders"

# --- Politeness & stability ---
USER_AGENT = os.getenv(
    "USER_AGENT",
    "PriceTrackProBot/1.0 (+contact: your_email@example.com)"
)
ROBOTSTXT_OBEY = True              # respect robots.txt
DOWNLOAD_DELAY = 1.0               # be polite; jitter added below
RANDOMIZE_DOWNLOAD_DELAY = True
CONCURRENT_REQUESTS = 8
RETRY_ENABLED = True
RETRY_TIMES = 2
AUTOTHROTTLE_ENABLED = True
FEED_EXPORT_ENCODING = "utf-8"

# --- Pipelines (order matters: lower number = earlier) ---
ITEM_PIPELINES = {
    "pricetrack_pro.pipelines.NormalizePipeline": 100,
    "pricetrack_pro.pipelines.StoreAndDiffPipeline": 200,
}

# --- Config via environment (.env optional) ---
DB_URL = os.getenv("DB_URL", "sqlite:///data/pricetrack.db")
ALERT_WEBHOOK_URL = os.getenv("ALERT_WEBHOOK_URL", "")