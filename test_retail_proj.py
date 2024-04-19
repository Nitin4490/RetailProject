import pytest
from lib.Utils import get_spark_session
from lib.DataReader import read_orders, read_customers
from lib.DataManipulation import filter_closed_orders, filter_orders_generic
from lib.ConfigReader import get_app_config

@pytest.mark.inputfile
def test_read_customer_df(spark):
    # spark = get_spark_session("LOCAL")
    customers_count = read_customers(spark, "LOCAL").count()
    assert customers_count ==12435

@pytest.mark.inputfile
def test_read_orders_df(spark):
    # spark = get_spark_session("LOCAL")
    orders_count = read_orders(spark, "LOCAL").count()
    assert orders_count == 68884

@pytest.mark.transformation
def test_filter_closed_orders(spark):
    # spark = get_spark_session("LOCAL")
    orders_df = read_orders(spark, "LOCAL")
    filtered_count = filter_closed_orders(orders_df).count()
    assert filtered_count == 7556

@pytest.mark.skip("work in progress")
def test_read_app_config():
    config_dict = get_app_config("LOCAL")
    assert config_dict["orders.file.path"] == "data/orders.csv"

# @pytest.mark.latest()
# def test_check_closed_count(spark):
#     orders_df = read_orders(spark, "LOCAL")
#     filtered_count = filter_orders_generic(orders_df, "CLOSED").count()
#     assert filtered_count == 7556



@pytest.mark.parametrize(
        "status,count",
        [("CLOSED",7556),
         ("PENDING_PAYMENT", 15030),
         ("COMPLETE", 22900)]
    )

def test_check_closed_count(spark, status, count):
    orders_df = read_orders(spark, "LOCAL")
    filtered_count = filter_orders_generic(orders_df, status).count()
    assert filtered_count == count
