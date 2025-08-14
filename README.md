# PriceTrack Pro
Automated Web Scraping & Price/Stock Monitoring with Alerts

PriceTrack Pro is a Python-based automation tool that scrapes e-commerce websites for product price and stock availability, stores the results in a database, and can trigger alerts when changes are detected.  
It also supports automatic daily runs using GitHub Actions.

## Features
- Web Scraping with [Scrapy](https://scrapy.org/)  
- Automation via GitHub Actions scheduler  
- SQLite Database storage for historical tracking  
- Change Detection for price and stock updates  
- Alert Integration (Slack/Discord via webhooks)  
- Configurable & Extensible for different sites  

## Tech Stack
- Python 3.11
- [Scrapy](https://scrapy.org/) — Web scraping framework
- [SQLite](https://www.sqlite.org/) — Lightweight database
- [sqlite-utils](https://sqlite-utils.datasette.io/) — Easy database querying
- [GitHub Actions](https://docs.github.com/en/actions) — Automation & scheduling
- [dotenv](https://pypi.org/project/python-dotenv/) — Environment variable management

## Project Structure
pricetrack-pro/
  .github/workflows/schedule.yml   # Daily GitHub Actions workflow
  data/                            # Database storage
  pricetrack_pro/                  # Scrapy project
    spiders/
      demo_store.py                 # Example spider
    items.py
    pipelines.py
    settings.py
  scripts/
    run.py                          # Local execution entry point
  requirements.txt
  scrapy.cfg
  README.md

## Quickstart

### 1. Clone the repository
git clone https://github.com/your-username/pricetrack-pro.git
cd pricetrack-pro

### 2. Create a virtual environment & install dependencies
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

pip install -r requirements.txt

### 3. Configure `.env`
ALERT_WEBHOOK_URL=   # Optional: Slack/Discord webhook
DB_URL=sqlite:///data/pricetrack.db
USER_AGENT=PriceTrackProBot/1.0 (+contact: your_email@example.com)

### 4. Run the scraper locally
python -m scripts.run

## Automation (GitHub Actions)
- The scraper runs daily at 09:00 Sydney Time (configurable in `.github/workflows/schedule.yml`).
- Run it manually from GitHub → Actions → daily-scrape → Run workflow.
- Scraped data is stored in `data/pricetrack.db` and uploaded as an artifact.

## Alerts
If `ALERT_WEBHOOK_URL` is set:
- You will receive a notification whenever product price or stock changes are detected.

## Example Use Cases
- Competitor Price Tracking
- E-commerce Stock Monitoring
- Market Trend Analysis
- Daily Price Alert Bots

## Skills Demonstrated
- Web scraping with Scrapy
- Automation pipelines with GitHub Actions
- Data storage & querying with SQLite
- Alert integrations with webhooks
- Git & GitHub best practices

## Results Preview
### Sample database tables
```
[{"table": "products"},
 {"table": "changes"},
 {"table": "sqlite_sequence"}]
```

### Sample product rows
```
[{"product_id": "a22124811bfa8350", "name": "It's Only the Himalayas", "price": 45.17, "in_stock": 1, "url": "https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html", "updated_at": "2025-08-13T08:47:23.033944"},
 {"product_id": "a18a4f574854aced", "name": "Libertarianism for Beginners", "price": 51.33, "in_stock": 1, "url": "https://books.toscrape.com/catalogue/libertarianism-for-beginners_982/index.html", "updated_at": "2025-08-13T08:47:24.253722"},
 {"product_id": "e30f54cea9b38190", "name": "Mesaerion: The Best Science Fiction Stories 1800-1849", "price": 37.59, "in_stock": 1, "url": "https://books.toscrape.com/catalogue/mesaerion-the-best-science-fiction-stories-1800-1849_983/index.html", "updated_at": "2025-08-13T08:47:25.893273"}]
```

### Query results
```
Number of products: 1000
Number of changes detected: 0
```