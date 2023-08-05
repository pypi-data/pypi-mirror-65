# django-simple-export-admin

A simple django admin allow your export queryset to xlsx file.


## Install

```shell
pip install django-simple-export-admin
```

## Usage


**pro/settings.py**

```python
INSTALLED_APPS = [
    ...
    'django_static_fontawesome',
    'django_changelist_toolbar_admin',
    'django_simple_export_admin',
    ...
]
```

- django_static_fontawesome, django_changelist_toolbar_admin and django_simple_export_admin are required.

**app/models.py**

```python
from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=32)
    author = models.CharField(max_length=32)
    is_published = models.NullBooleanField()
    published_date = models.DateField(null=True)

    class Meta:
        permissions = [
            ("export_filtered_books", "Export all filtered books"),
        ]
```


**app/admin.py**


```python
from django.contrib import admin
from django_simple_export_admin.admin import DjangoSimpleExportAdmin
from django_simple_export_admin.admin import NullBooleanRender
from django_simple_export_admin.admin import DateRender
from django_simple_export_admin.admin import Sum
from .models import Book

class BookAdmin(DjangoSimpleExportAdmin, admin.ModelAdmin):
    list_display = ["name", "author"]
    list_filter = ["is_published", "published_date", "author"]

    django_simple_export_admin_exports = {
        "filtered-books": {
            "label": "Export All Filtered Books",
            "icon": "fas fa-book",
            "filename": "Book",
            "fields": [
                {"field": "__row_index", "label": "Index"},
                {"field": "name", "label": "Book Name", "footer-value": "Sum:"},
                {"field": "count", "label": "Stock", "footer-value": lambda: Sum()},
                {"field": "author", "label": "Author", "empty_value": "-"},
                {"field": "is_published", "label": "Is Published", "render": NullBooleanRender("UNKNOWN", "YES", "NO")},
                {"field": "published_date", "label": "Published Date", "render": DateRender()},
            ],
            "export-filtered": True,
            "permissions": ["django_simple_export_admin_example.export_filtered_books"],
        }
    }

```

- `label` default to _("Export").
- `icon` default to None means no icon.
- `filename` default to model_name.
- `export-filtered` default to False, means always export all queryset without filtering.
- `permissions` default to None, means only super admin have permission to do exporting.
- `fields`
    - `field == __row_index` will always display row index, e.g. 1,2,3...
    - `render` is a callable object that transform the original value to display value.
    - `empty_value` only works when `render` is not provided, it is the display value for orignal None value.
    - `field` can be field of the model instance, callable function of the model instance, callable function of the admin which takes model instance parameter. Similar with field name in `list_display`.
    - `footer-value` is the value display at the bottom row. It can be an instance of Aggregate that accept every item value of this field and calc the final value at last. It can be a staic value.


## Shipped Renders

- django_simple_export_admin.admin.DateRender
- django_simple_export_admin.admin.BooleanRender
- django_simple_export_admin.admin.NullBooleanRender

## Shipped Aggregates

- django_simple_export_admin.admin.Sum
- django_simple_export_admin.admin.Average
- django_simple_export_admin.admin.Count

## Releases

### v0.1.2 2020/04/02

- Fix document.

### v0.1.1 2020/04/02

- Fix footer-value problem. If use an instance of Aggregate in settings, the instance is used globally, so that the final value if not correct. So you must add lambda to dynamically to create a new instance very time.

### v0.1.0 2020/04/02

- First release.