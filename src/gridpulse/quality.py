# src/gridpulse/quality.py
READING_RULES_DROP = {
    "valid_meter_id": "meter_id IS NOT NULL AND meter_id LIKE 'MTR-%'",
    "valid_timestamp": "reading_ts IS NOT NULL AND reading_ts > '2020-01-01'",
}
READING_RULES_WARN = {
    "plausible_kwh": "kwh BETWEEN 0 AND 50",
    "plausible_voltage": "voltage BETWEEN 180 AND 260",
}
READING_RULES_FAIL = {
    "no_future_readings": "reading_ts <= current_timestamp() + INTERVAL 1 DAY",
}

def quarantine_condition(rules: dict) -> str:
    """Return SQL that is TRUE when ANY rule fails — used to route bad rows to quarantine."""
    return "NOT (" + " AND ".join(f"({r})" for r in rules.values()) + ")"
