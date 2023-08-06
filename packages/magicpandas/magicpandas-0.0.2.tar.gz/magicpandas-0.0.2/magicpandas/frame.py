import subprocess
import os
import warnings
import numpy as np
import pandas as pd
import functools
from magicpandas.utils import search_iterable
from magicpandas.easy_xlsxwriter import easy_xlsxwriter
import altair as alt
from magicpandas.chromify import chromify


class MagicSeries(pd.Series):
    @property
    def _constructor(self):
        return MagicSeries

    @property
    def _constructor_expanddim(self):
        return MagicDataFrame


class MagicDataFrame(pd.DataFrame):
    @property
    def _constructor(self):
        return MagicDataFrame

    @property
    def _constructor_sliced(self):
        return MagicSeries

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        with warnings.catch_warnings():
            # The usual warning: Pandas doesn't allow columns to be created via a new attribute name
            warnings.simplefilter("ignore")
            self.verbose_labels = {x:x for x in self.columns}  # By default, labels are the same as the column names

    def set_verbose_labels(self, new_verbose_labels: dict) -> None:
        """Modify labels"""
        self.verbose_labels.update(new_verbose_labels)

    def clear_verbose_labels(self):
        """Clear all labels i.e., set labels to column name"""
        self.verbose_labels = {x:x for x in self.columns}  # By default, labels are the same as the column names

    def drop(self, labels=None, axis=0, index=None, columns=None, level=None, inplace=False, errors="raise"):
        try:
            return super().drop(labels, axis, index, columns, level, inplace, errors)
        except KeyError as e:
            if str(e)[-18:-1]=="not found in axis":  # make sure it's not some other KeyError
                if labels and axis==0:
                    labels = search_iterable(self.index, labels)
                elif labels and axis==1:
                    labels = search_iterable(self.columns, labels)
                elif index:
                    index = search_iterable(self.index, index)
                elif columns:
                    columns = search_iterable(self.columns, columns)
                else:
                    raise KeyError(e)
            return super().drop(labels, axis, index, columns, level, inplace, errors)

    def browse(self, path: str=None, limit: int=None, run: bool=True, percentage_columns: list=None, autofit_columns: list=None, client: str='excel') -> None:
        if client=="excel":
            easy_xlsxwriter(self, path, limit, run, percentage_columns, autofit_columns)
        elif client=="webbrowser":
            # UNDER CONSTRUCTION
            from magicpandas.chromify import chromify
            chromify(self.to_html(), path, run)
        else:
            raise ValueError('Argument "client" must be either excel or webbrowser')

    def inspect_for_django(self, model_name='DjangoModel'):
        result = ''
        for label, verbose_label in self.verbose_labels.items():
        # for index, row in self.verbose_labels.iterrows():
            try:
                if self.dtypes[label] == 'object':  # i.e., a string
                    result += f"""    {label} = models.CharField(max_length=255, verbose_name="{verbose_label}", null=True)\n"""
                elif self.dtypes[label] == 'float64':
                    result += f"""    {label} = models.FloatField(verbose_name="{verbose_label}", null=True)\n"""
                elif self.dtypes[label] == 'datetime64[ns]':
                    result += f"""    {label} = models.DateField(verbose_name="{verbose_label}", null=True)\n"""
                elif self.dtypes[label] == 'bool':
                    result += f"""    {label} = models.BooleanField(verbose_name="{verbose_label}", null=True)\n"""
                elif self.dtypes[label] == 'int64':
                    result += f"""    {label} = models.BigIntegerField(verbose_name="{verbose_label}", null=True)\n"""
                else:
                    raise Exception(f"{label}: There is currently no support for type {self.dtypes[label]}")
            except KeyError as e:
                import warnings
                warnings.warn(f"{label} appears to be in the key file but not in the data file.", stacklevel=2)
        print(f'class {model_name}(models.Model):')
        print(result)

    def to_django(self, DjangoModel, if_exists='fail'):
        """Uses bulk_create to insert data to Django table
        if_exists: see pd.DataFrame.to_sql API

        Ref: https://www.webforefront.com/django/multiplemodelrecords.html
        """
        # TODO: How to I test this?
        if not if_exists in ['fail', 'replace', 'append']:
            raise Exception('if_exists must be fail, replace or append')

        if if_exists=="replace":
            DjangoModel.objects.all().delete()
        elif if_exists=="fail":
            if DjangoModel.objects.all().count()>0:
                raise ValueError('Data already exists in this table')
        else:
            pass

        dct = self.replace({np.nan: None}).to_dict('records') # replace NaN with None since Django doesn't understand NaN

        bulk_list = []
        for x in dct:
            bulk_list.append(DjangoModel(**x))
        DjangoModel.objects.bulk_create(bulk_list)
        print('Successfully saved DataFrame to Django table.')

    def scatter(self, *args, **kwargs):
        """Opens a graph in Chrome using the excellent Altair library"""
        chart = alt.Chart(self).mark_circle().encode(*args, **kwargs)
        chromify(chart.to_html())
