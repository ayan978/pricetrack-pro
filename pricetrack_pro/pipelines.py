import os, json, sqlite3, urllib.request
from datetime import datetime
from typing import Dict, Any
from .items import Product
from . import settings as cfg

DB_PATH = cfg.DB_URL.replace("sqlite:///", "")

class NormalizePipeline:
    def process_item(self, item: Dict[str, Any], spider):
        model = Product(**item)  # validate & coerce types
        return model.model_dump()

class StoreAndDiffPipeline:
    def open_spider(self, spider):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self.cur = self.conn.cursor()
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
          product_id TEXT PRIMARY KEY,
          name TEXT,
          price REAL,
          in_stock INTEGER,
          url TEXT,
          updated_at TEXT
        )
        """)
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS changes (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          product_id TEXT,
          field TEXT,
          old_value TEXT,
          new_value TEXT,
          changed_at TEXT
        )
        """)
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def _alert(self, text: str):
        if not cfg.ALERT_WEBHOOK_URL:
            return
        try:
            data = json.dumps({"text": text}).encode("utf-8")
            req = urllib.request.Request(
                cfg.ALERT_WEBHOOK_URL,
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            urllib.request.urlopen(req, timeout=10)
        except Exception:
            pass  # don't break the crawl if alert fails

    def process_item(self, item, spider):
        now = datetime.utcnow().isoformat()
        item["updated_at"] = now

        self.cur.execute(
            "SELECT name, price, in_stock, url FROM products WHERE product_id = ?",
            (item["product_id"],)
        )
        row = self.cur.fetchone()

        if row is None:
            self.cur.execute(
                "INSERT INTO products(product_id, name, price, in_stock, url, updated_at) VALUES (?,?,?,?,?,?)",
                (item["product_id"], item["name"], item["price"], int(item["in_stock"]),
                 item["url"], item["updated_at"])
            )
        else:
            prev = {"name": row[0], "price": row[1], "in_stock": bool(row[2]), "url": row[3]}
            diffs = []
            if (prev["price"] is None) != (item["price"] is None) or (prev["price"] or 0) != (item["price"] or 0):
                diffs.append(("price", prev["price"], item["price"]))
            if bool(prev["in_stock"]) != bool(item["in_stock"]):
                diffs.append(("in_stock", prev["in_stock"], item["in_stock"]))

            if diffs:
                self.cur.execute(
                    "UPDATE products SET name=?, price=?, in_stock=?, url=?, updated_at=? WHERE product_id=?",
                    (item["name"], item["price"], int(item["in_stock"]), item["url"],
                     item["updated_at"], item["product_id"])
                )
                for field, old, new in diffs:
                    self.cur.execute(
                        "INSERT INTO changes(product_id, field, old_value, new_value, changed_at) VALUES (?,?,?,?,?)",
                        (item["product_id"], field, str(old), str(new), now)
                    )
                # Optional: send alert
                lines = [f"Change detected for {item['name']} ({item['product_id']}):"]
                for f, o, n in diffs:
                    lines.append(f"- {f}: {o} → {n}")
                lines.append(f"URL: {item['url']}")
                self._alert("\n".join(lines))

        return item