# from magicpandas.utils import search_iterable
from ..frame import MagicDataFrame
import warnings
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    import statsmodels.api as sm

def test_drop_columns():
    df = sm.datasets.get_rdataset("Duncan", "carData").data
    df = MagicDataFrame(df)
    df = df.drop('*e', axis=1)  # drop any column that ends with e
    assert df.columns[0]=='education'
    assert len(df.columns)==1
