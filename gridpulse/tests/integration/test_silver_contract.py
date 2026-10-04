from pyspark.testing import assertSchemaEqual
expected = spark.table("gridpulse.silver.readings").limit(0).schema  # snapshot you approved
actual = spark.table("gridpulse.silver.readings").schema
assertSchemaEqual(actual, expected)
assert spark.table("gridpulse.silver.readings").filter("meter_id IS NULL").count() == 0, "null meter ids leaked"
