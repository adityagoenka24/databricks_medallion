# src/gridpulse/transforms.py
from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def standardise_meter_id(df: DataFrame, col: str = "meter_id") -> DataFrame:
    """Upper-case and trim meter IDs: ' mtr-00012 ' -> 'MTR-00012'."""
    return df.withColumn(col, F.upper(F.trim(F.col(col))))


def add_reading_date(df: DataFrame, ts_col: str = "reading_ts") -> DataFrame:
    """Derive a DATE column used for grain/partition-style filters."""
    return df.withColumn("reading_date", F.to_date(F.col(ts_col)))


def flag_negative_kwh(df: DataFrame) -> DataFrame:
    """Meters should never report negative consumption; flag instead of drop (keep evidence)."""
    return df.withColumn("is_negative_kwh", F.col("kwh") < 0)


def kwh_to_cost(df: DataFrame, rate_col: str = "rate_aed_per_kwh") -> DataFrame:
    """Compute cost in AED, rounded to 2 decimals."""
    return df.withColumn("cost_aed", F.round(F.col("kwh") * F.col(rate_col), 2))


def clean_readings(df: DataFrame) -> DataFrame:
    """Composite transform — chain with DataFrame.transform for readability."""
    return (df.transform(standardise_meter_id)
              .transform(add_reading_date)
              .transform(flag_negative_kwh))
