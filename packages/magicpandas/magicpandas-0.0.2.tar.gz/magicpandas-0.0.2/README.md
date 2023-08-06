\#\#\#\#\# UNDER CONSTRUCTION \#\#\#\#\# 

### magicpandas
*magicpandas* makes working with pandas dead simple.

### Main Features
* MagicDataFrame subclasses DataFrame to make existing methods more intuitive as well as add new methods
* MagicDataFrame adds verbose labels that are used by default when displaying data
* MagicDataFrame supports Django ORM  
  * inspectdf uses DataFrame column types to produce a Django model class (cf. [inspectdb](https://docs.djangoproject.com/en/3.0/howto/legacy-databases/#auto-generate-the-models))
  * to_django saves the DataFrame to SQL using Django ORM's [bulk_update](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#bulk-update) and [bulk_create](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#bulk-create).

##### Examples
```python
df2 = df.drop('*e', axis=1) # df2 drops all columns ending in "e"
df.browse() # opens the DataFrame in MS Excel with nice formatting
df.browse(client='webbrowser') # opens the DataFrame as html displayed in Chrome with nice formatting
```

### TODO
* chromify(chart.to_html())
* inspect_as_django_model
* to_django
