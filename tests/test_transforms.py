# tests/test_transforms.py
import datetime as dt
from pyspark.sql import Row
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, DoubleType, DateType, BooleanType
from pyspark.testing import assertDataFrameEqual, assertSchemaEqual

from gridpulse.transforms import standardise_meter_id, add_reading_date, clean_readings, kwh_to_cost


def test_standardise_meter_id(spark):
    df = spark.createDataFrame([(" mtr-00012 ",), ("MTR-00013",)], ["meter_id"])
    actual = df.transform(standardise_meter_id)
    expected = spark.createDataFrame([("MTR-00012",), ("MTR-00013",)], ["meter_id"])
    assertDataFrameEqual(actual, expected)          # order-insensitive by default


def test_kwh_to_cost_rounding(spark):
    df = spark.createDataFrame([(1.234, 0.3)], ["kwh", "rate_aed_per_kwh"])
    actual = df.transform(kwh_to_cost)
    expected = spark.createDataFrame([(1.234, 0.3, 0.37)], ["kwh", "rate_aed_per_kwh", "cost_aed"])
    assertDataFrameEqual(actual, expected, rtol=1e-5)   # tolerance for floats


def test_clean_readings_schema(spark):
    src_schema = StructType([
        StructField("meter_id", StringType()),
        StructField("reading_ts", TimestampType()),
        StructField("kwh", DoubleType()),
    ])
    df = spark.createDataFrame([("mtr-1", dt.datetime(2026, 10, 1, 10, 15), -0.5)], src_schema)
    actual = df.transform(clean_readings)
    expected_schema = StructType(src_schema.fields + [
        StructField("reading_date", DateType()),
        StructField("is_negative_kwh", BooleanType()),
    ])
    assertSchemaEqual(actual.schema, expected_schema)   # catches accidental schema drift
    assert actual.first()["is_negative_kwh"] is True
