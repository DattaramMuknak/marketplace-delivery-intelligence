import pandas as pd

DATE_FORMATS = ["%d-%m-%y", "%d-%m-%Y", "%d/%m/%Y", "%d/%m/%y", "%Y-%m-%d"]

def parse_mixed_dates(series):
    return pd.to_datetime(series, errors="coerce", dayfirst=True, format="mixed")

def normalize_courier(value):
    raw = str(value).strip()
    key = raw.lower().replace(" ", "").replace("-", "")
    mapping = {
        "shipquick": "ShipQuick",
        "fastbee": "FastBee",
        "bluedart": "Blue Dart",
    }
    return mapping.get(key, raw.title())

def analyze_deliveries(raw_df):
    required = {"order_id", "shipped_at", "delivered_at", "courier", "promised_days", "is_test_order"}
    missing = required - set(raw_df.columns)
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))

    df = raw_df.copy()
    warnings = []
    for col in ["shipped_at", "delivered_at", "updated_at", "order_date"]:
        if col in df.columns:
            df[col] = parse_mixed_dates(df[col])

    df["courier"] = df["courier"].map(normalize_courier)
    df["is_test_order_norm"] = df["is_test_order"].astype(str).str.strip().str.lower().isin(["yes", "true", "1", "y"])
    df["promised_days"] = pd.to_numeric(df["promised_days"], errors="coerce")

    before = len(df)
    # Keep latest version of each order record where possible.
    sort_cols = ["order_id"] + (["updated_at"] if "updated_at" in df.columns else [])
    df = df.sort_values(sort_cols, na_position="first").drop_duplicates("order_id", keep="last")
    if len(df) < before:
        warnings.append(f"Removed {before-len(df)} duplicate order record(s), keeping the latest updated record per order_id.")

    # Scope is based on delivered_at in May 2026, as specified by the task.
    may_mask = df["delivered_at"].between(pd.Timestamp("2026-05-01"), pd.Timestamp("2026-05-31 23:59:59"))
    candidates = df.loc[may_mask].copy()
    if candidates["is_test_order_norm"].any():
        warnings.append("Excluded test/internal orders.")
    candidates = candidates.loc[~candidates["is_test_order_norm"]]
    if "order_status" in candidates.columns:
        candidates = candidates.loc[candidates["order_status"].astype(str).str.strip().str.lower().eq("delivered")]
    candidates["actual_transit_days"] = (candidates["delivered_at"] - candidates["shipped_at"]).dt.total_seconds() / 86400
    valid = (
        candidates["shipped_at"].notna()
        & candidates["delivered_at"].notna()
        & candidates["promised_days"].notna()
        & candidates["promised_days"].gt(0)
        & candidates["actual_transit_days"].ge(0)
    )
    invalid_count = int((~valid).sum())
    if invalid_count:
        warnings.append(f"Excluded {invalid_count} record(s) with missing dates, negative transit, or invalid/non-positive promised_days.")
    clean = candidates.loc[valid].copy()
    clean["delivery_status"] = clean.apply(
        lambda r: "On Time" if r["actual_transit_days"] <= r["promised_days"] else "Late", axis=1
    )
    clean["actual_transit_days"] = clean["actual_transit_days"].round(2)

    if clean.empty:
        summary = pd.DataFrame(columns=["courier", "eligible_orders", "on_time_orders", "on_time_rate"])
    else:
        summary = clean.groupby("courier", as_index=False).agg(
            eligible_orders=("order_id", "nunique"),
            on_time_orders=("delivery_status", lambda s: int((s == "On Time").sum()))
        )
        summary["on_time_rate"] = summary["on_time_orders"] / summary["eligible_orders"]
        summary = summary.sort_values(["on_time_rate", "eligible_orders"], ascending=[False, False]).reset_index(drop=True)

    if "city" in clean.columns:
        clean["city"] = clean["city"].astype(str).str.strip().replace({"Bangalore":"Bengaluru", "bangalore":"Bengaluru"})
    return {"clean": clean, "summary": summary, "warnings": warnings}

def clean_uploaded_data(df):
    return df.copy()

def build_charts_data(df):
    return df
