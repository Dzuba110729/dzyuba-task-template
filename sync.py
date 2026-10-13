import json
import os
import re
import urllib.request
from datetime import datetime

ORDERS_URL = os.getenv("ORDERS_URL", "https://test.ooobs.ru/api/orders")


def fetch_orders() -> list[dict]:
    with urllib.request.urlopen(ORDERS_URL, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def normalize_phone(raw) -> str | None:
    digits = re.sub(r"\D", "", str(raw or ""))
    if len(digits) == 10 and digits.startswith("9"):
        digits = "7" + digits
    if len(digits) == 11 and digits[0] in "78":
        return "+7" + digits[1:]
    return None


def to_amount(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def to_time(value) -> datetime:
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return datetime.min


def build_result(orders: list[dict]) -> dict:
    best: dict[str, dict] = {}
    invalid = 0
    valid = 0
    for order in orders:
        phone = normalize_phone(order.get("phone"))
        if phone is None:
            invalid += 1
            continue
        valid += 1
        current = best.get(phone)
        key = (to_amount(order.get("amount")), to_time(order.get("created_at")))
        if current is None or key > current["_key"]:
            best[phone] = {"_key": key, "order": order, "phone": phone}

    clients = []
    for item in best.values():
        order = item["order"]
        amount = to_amount(order.get("amount"))
        clients.append({
            "name": order.get("name") or "",
            "phone": item["phone"],
            "email": order.get("email") or "",
            "amount": int(amount) if amount.is_integer() else amount,
        })
    clients.sort(key=lambda c: c["phone"])

    return {
        "clients": clients,
        "stats": {
            "received": len(orders),
            "unique": len(clients),
            "duplicates_merged": valid - len(clients),
            "invalid_dropped": invalid,
        },
    }
