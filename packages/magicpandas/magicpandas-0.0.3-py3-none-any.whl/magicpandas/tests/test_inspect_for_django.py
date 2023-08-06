# from magicpandas.utils import search_iterable
from magicpandas.frame import MagicDataFrame
import os
import warnings
from contextlib import suppress
from magicpandas.easy_xlsxwriter import easy_xlsxwriter
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    import statsmodels.api as sm

from contextlib import redirect_stdout
import io

def test_inspect_for_django():
    df = sm.datasets.get_rdataset("Duncan", "carData").data
    df = MagicDataFrame(df)
    f = io.StringIO()
    with redirect_stdout(f):
        df.inspect_for_django()
    correct_output = """class DjangoModel(models.Model):
    type = models.CharField(max_length=255, verbose_name="type", null=True)
    income = models.BigIntegerField(verbose_name="income", null=True)
    education = models.BigIntegerField(verbose_name="education", null=True)
    prestige = models.BigIntegerField(verbose_name="prestige", null=True)

"""
    assert f.getvalue()==correct_output
