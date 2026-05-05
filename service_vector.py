import numpy as np
from datetime import datetime

#TODO get config and mcc risk from files in resources
CONFIG = {
    "max_amount": 10000.0,
    "max_installments": 12.0,
    "amount_vs_avg_ratio": 10.0,
    "max_minutes": 1440.0,
    "max_km": 1000.0,
    "max_tx_count_24h": 50.0,
    "max_merchant_avg_amount": 1000.0,
    "mcc_risk_default": 0.5
}

MCC_RISK_MAP = {
    "5411": 0.2,
    "5812": 0.4,
    "7995": 0.9,
    "7801": 0.7
}

def clamp(x):
    return np.clip(x, 0.0, 1.0)

def vectorize_transaction(data: dict) -> np.ndarray:
    tx = data.get("transaction", {})
    cust = data.get("customer", {})
    merch = data.get("merchant", {})
    term = data.get("terminal", {})
    last_tx = data.get("last_transaction")

    
    dt = datetime.strptime(tx["requested_at"], "%Y-%m-%dT%H:%M:%S%z")
    
    v0 = clamp(tx["amount"] / CONFIG["max_amount"])
    v1 = clamp(tx["installments"] / CONFIG["max_installments"])
    v2 = clamp((tx["amount"] / cust["avg_amount"]) / CONFIG["amount_vs_avg_ratio"])

    v3 = dt.hour / 23.0
    v4 = dt.weekday() / 6.0

    if last_tx:
        last_dt = datetime.strptime(last_tx["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
        diff_minutes = abs((dt - last_dt).total_seconds() / 60.0)
        v5 = clamp(diff_minutes / CONFIG["max_minutes"])
    else:
        v5 = -1.0

    v6 = clamp(last_tx["km_from_current"] / CONFIG["max_km"]) if last_tx else -1.0

    v7 = clamp(term["km_from_home"] / CONFIG["max_km"])
    v8 = clamp(cust["tx_count_24h"] / CONFIG["max_tx_count_24h"])

    v9 = 1.0 if term.get("is_online") else 0.0
    v10 = 1.0 if term.get("card_present") else 0.0
    v11 = 0.0 if merch["id"] in cust.get("known_merchants", []) else 1.0

    v12 = MCC_RISK_MAP.get(merch["mcc"], CONFIG["mcc_risk_default"])
    v13 = clamp(merch["avg_amount"] / CONFIG["max_merchant_avg_amount"])

    return np.array([v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13], dtype=np.float32)