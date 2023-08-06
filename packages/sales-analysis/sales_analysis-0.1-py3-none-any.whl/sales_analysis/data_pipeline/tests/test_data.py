from sales_analysis.data_pipeline import BASEPATH
from sales_analysis.data_pipeline._pipeline import SalesPipeline

import pytest
import os
import pandas as pd

# --------------------------------------------------------------------------
# Fixtures

@pytest.fixture
def pipeline():
    FILEPATH = os.path.join(BASEPATH, "data")
    DATA_FILES = [f for f in os.listdir(FILEPATH) if f.endswith('.csv')]
    DATA = {f : pd.read_csv(os.path.join(FILEPATH, f)) for f in DATA_FILES}

    return SalesPipeline(**DATA)

# --------------------------------------------------------------------------
# Data 

data = {'customers': {pd.Timestamp('2019-08-01 00:00:00'): 9,
                      pd.Timestamp('2019-08-02 00:00:00'): 10,
                      pd.Timestamp('2019-08-03 00:00:00'): 10,
                      pd.Timestamp('2019-08-04 00:00:00'): 10,
                      pd.Timestamp('2019-08-05 00:00:00'): 9,
                      pd.Timestamp('2019-08-06 00:00:00'): 9,
                      pd.Timestamp('2019-08-07 00:00:00'): 10,
                      pd.Timestamp('2019-08-08 00:00:00'): 8,
                      pd.Timestamp('2019-08-09 00:00:00'): 5,
                      pd.Timestamp('2019-08-10 00:00:00'): 5,
                      pd.Timestamp('2019-08-11 00:00:00'): 10,
                      pd.Timestamp('2019-08-12 00:00:00'): 10,
                      pd.Timestamp('2019-08-13 00:00:00'): 6,
                      pd.Timestamp('2019-08-14 00:00:00'): 7,
                      pd.Timestamp('2019-08-15 00:00:00'): 10,
                      pd.Timestamp('2019-08-16 00:00:00'): 8,
                      pd.Timestamp('2019-08-17 00:00:00'): 7,
                      pd.Timestamp('2019-08-18 00:00:00'): 9,
                      pd.Timestamp('2019-08-19 00:00:00'): 5,
                      pd.Timestamp('2019-08-20 00:00:00'): 5},
 'total_discount_amount': {pd.Timestamp('2019-08-01 00:00:00'): 15152814.736907512,
                        pd.Timestamp('2019-08-02 00:00:00'): 20061245.64408109,
                        pd.Timestamp('2019-08-03 00:00:00'): 26441693.751396574,
                        pd.Timestamp('2019-08-04 00:00:00'): 25783015.567048658,
                        pd.Timestamp('2019-08-05 00:00:00'): 16649773.993076814,
                        pd.Timestamp('2019-08-06 00:00:00'): 24744027.428384878,
                        pd.Timestamp('2019-08-07 00:00:00'): 21641181.771564845,
                        pd.Timestamp('2019-08-08 00:00:00'): 27012160.85245146,
                        pd.Timestamp('2019-08-09 00:00:00'): 13806814.237002019,
                        pd.Timestamp('2019-08-10 00:00:00'): 9722459.599448118,
                        pd.Timestamp('2019-08-11 00:00:00'): 20450260.26194652,
                        pd.Timestamp('2019-08-12 00:00:00'): 22125711.151501,
                        pd.Timestamp('2019-08-13 00:00:00'): 11444206.200090334,
                        pd.Timestamp('2019-08-14 00:00:00'): 17677326.65707852,
                        pd.Timestamp('2019-08-15 00:00:00'): 26968819.12338184,
                        pd.Timestamp('2019-08-16 00:00:00'): 22592246.991756547,
                        pd.Timestamp('2019-08-17 00:00:00'): 15997597.519811645,
                        pd.Timestamp('2019-08-18 00:00:00'): 17731498.506244037,
                        pd.Timestamp('2019-08-19 00:00:00'): 22127822.876592986,
                        pd.Timestamp('2019-08-20 00:00:00'): 5550506.789972418},
 'items': {pd.Timestamp('2019-08-01 00:00:00'): 2895,
        pd.Timestamp('2019-08-02 00:00:00'): 3082,
        pd.Timestamp('2019-08-03 00:00:00'): 3559,
        pd.Timestamp('2019-08-04 00:00:00'): 3582,
        pd.Timestamp('2019-08-05 00:00:00'): 2768,
        pd.Timestamp('2019-08-06 00:00:00'): 3431,
        pd.Timestamp('2019-08-07 00:00:00'): 2767,
        pd.Timestamp('2019-08-08 00:00:00'): 2643,
        pd.Timestamp('2019-08-09 00:00:00'): 1506,
        pd.Timestamp('2019-08-10 00:00:00'): 1443,
        pd.Timestamp('2019-08-11 00:00:00'): 2466,
        pd.Timestamp('2019-08-12 00:00:00'): 3482,
        pd.Timestamp('2019-08-13 00:00:00'): 1940,
        pd.Timestamp('2019-08-14 00:00:00'): 1921,
        pd.Timestamp('2019-08-15 00:00:00'): 3479,
        pd.Timestamp('2019-08-16 00:00:00'): 3053,
        pd.Timestamp('2019-08-17 00:00:00'): 2519,
        pd.Timestamp('2019-08-18 00:00:00'): 2865,
        pd.Timestamp('2019-08-19 00:00:00'): 1735,
        pd.Timestamp('2019-08-20 00:00:00'): 1250},
 'order_total_avg': {pd.Timestamp('2019-08-01 00:00:00'): 1182286.0960463749,
                    pd.Timestamp('2019-08-02 00:00:00'): 1341449.559055637,
                    pd.Timestamp('2019-08-03 00:00:00'): 1270616.0372525519,
                    pd.Timestamp('2019-08-04 00:00:00'): 1069011.1516039693,
                    pd.Timestamp('2019-08-05 00:00:00'): 1355304.7342628485,
                    pd.Timestamp('2019-08-06 00:00:00'): 1283968.435650978,
                    pd.Timestamp('2019-08-07 00:00:00'): 1319110.4787216866,
                    pd.Timestamp('2019-08-08 00:00:00'): 1027231.5196824896,
                    pd.Timestamp('2019-08-09 00:00:00'): 1201471.0717715647,
                    pd.Timestamp('2019-08-10 00:00:00'): 1314611.2300065856,
                    pd.Timestamp('2019-08-11 00:00:00'): 1186152.4565363638,
                    pd.Timestamp('2019-08-12 00:00:00'): 1155226.4552911327,
                    pd.Timestamp('2019-08-13 00:00:00'): 1346981.8930212667,
                    pd.Timestamp('2019-08-14 00:00:00'): 1019646.0386455443,
                    pd.Timestamp('2019-08-15 00:00:00'): 1286793.278547962,
                    pd.Timestamp('2019-08-16 00:00:00'): 1254721.8660029566,
                    pd.Timestamp('2019-08-17 00:00:00'): 1419237.673786449,
                    pd.Timestamp('2019-08-18 00:00:00'): 1173087.9508403398,
                    pd.Timestamp('2019-08-19 00:00:00'): 1162434.8033358732,
                    pd.Timestamp('2019-08-20 00:00:00'): 1046669.750923031},
'discount_rate_avg': {pd.Timestamp('2019-08-01 00:00:00'): 0.1252497888814673,
                    pd.Timestamp('2019-08-02 00:00:00'): 0.12950211356271726,
                    pd.Timestamp('2019-08-03 00:00:00'): 0.1490744307031331,
                    pd.Timestamp('2019-08-04 00:00:00'): 0.15162918618667656,
                    pd.Timestamp('2019-08-05 00:00:00'): 0.13130630218741238,
                    pd.Timestamp('2019-08-06 00:00:00'): 0.13373546744128126,
                    pd.Timestamp('2019-08-07 00:00:00'): 0.15567735848995318,
                    pd.Timestamp('2019-08-08 00:00:00'): 0.20265603603112725,
                    pd.Timestamp('2019-08-09 00:00:00'): 0.17727372441724282,
                    pd.Timestamp('2019-08-10 00:00:00'): 0.1420197829256685,
                    pd.Timestamp('2019-08-11 00:00:00'): 0.15144502071841046,
                    pd.Timestamp('2019-08-12 00:00:00'): 0.12961399577196853,
                    pd.Timestamp('2019-08-13 00:00:00'): 0.12731849238164458,
                    pd.Timestamp('2019-08-14 00:00:00'): 0.20101097686303473,
                    pd.Timestamp('2019-08-15 00:00:00'): 0.14895723666327493,
                    pd.Timestamp('2019-08-16 00:00:00'): 0.12871697115230343,
                    pd.Timestamp('2019-08-17 00:00:00'): 0.14041300964840808,
                    pd.Timestamp('2019-08-18 00:00:00'): 0.13535199553408908,
                    pd.Timestamp('2019-08-19 00:00:00'): 0.21438859223995432,
                    pd.Timestamp('2019-08-20 00:00:00'): 0.11914043920600781}}

# --------------------------------------------------------------------------
# Tests

@pytest.mark.parametrize(
    "attribute", 
    [
        ("orders"), 
        ("commissions"), 
        ("order_lines"), 
        ("product_promotions"), 
        ("products"), 
        ("promotions")
    ]
)
def test_instance(pipeline, attribute):
    assert hasattr(pipeline, attribute)

@pytest.mark.parametrize("solution", [data])
def test_summary(pipeline, solution):
    summary = pipeline.summary() 
    assert summary.iloc[:20].equals(pd.DataFrame.from_dict(data))