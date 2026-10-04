"""This file configures pytest, initializes Databricks Connect, and provides fixtures for Spark and loading test data."""

import os, sys, pathlib
from contextlib import contextmanager


try:
    from pyspark.sql import SparkSession
    import pytest
    import json
    import csv
    import os
except ImportError:
    raise ImportError(
        "Test dependencies not found.\n\nRun tests using 'uv run pytest'. See http://docs.astral.sh/uv to learn more about uv."
    )


@pytest.fixture()
def spark() -> SparkSession:

    # return DatabricksSession.builder.getOrCreate()

    return (SparkSession.builder.master("local[2]")
            .appName("gridpulse-tests")
            .config("spark.sql.session.timeZone", "UTC")
            .getOrCreate())
