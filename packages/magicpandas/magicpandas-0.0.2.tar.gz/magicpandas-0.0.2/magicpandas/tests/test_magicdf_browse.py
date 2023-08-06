# from magicpandas.utils import search_iterable
from magicpandas.frame import MagicDataFrame
import os
import warnings
from contextlib import suppress
from magicpandas.easy_xlsxwriter import easy_xlsxwriter
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    import statsmodels.api as sm

def test_browse_in_excel():
    """Test that MagicDataFrame.browse creates an xlsx file in the temp directory"""
    import tempfile
    path_to_check = os.path.join(tempfile.gettempdir(), 'easy_xlsxwriter.xlsx')
    with suppress(FileNotFoundError):
        os.remove(path_to_check)
    df = sm.datasets.get_rdataset("Duncan", "carData").data
    df = MagicDataFrame(df)
    df.browse(client='excel', run=False)
    assert os.path.exists(path_to_check)

def test_browse_in_webbrowser():
    """Test that MagicDataFrame.browse creates an xlsx file in the temp directory"""
    import tempfile
    path_to_check = os.path.join(tempfile.gettempdir(), 'magicpandas_chromify.html')
    with suppress(FileNotFoundError):
        os.remove(path_to_check)
    df = sm.datasets.get_rdataset("Duncan", "carData").data
    df = MagicDataFrame(df)
    df.browse(client='webbrowser', run=False)
    assert os.path.exists(path_to_check)
