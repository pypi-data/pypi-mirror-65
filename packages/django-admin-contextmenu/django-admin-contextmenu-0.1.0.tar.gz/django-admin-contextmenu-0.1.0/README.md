django-admin-contextmenu
=======================

This is a multi-directional context menu for Django admin. It adds a new column in your admin's changelist page, after the checkbox column. When it is clicked a pop menu opens. The menu is completely empty and it is the best place for including links to other entites.


Requirements
-----------------------------

* Django > 2.2
* Python > 3.5


Installation
------------

Use your favorite Python package manager to install the app from PyPI, e.g.

Example:

``pip install django-admin-contextmenu``


Add ``contextmenu`` to ``INSTALLED_APPS``:

Example:

```python

    INSTALLED_APPS = (
        ...
        'contextmenu',
        ...
    )
```


Example usage in admin
-------------

```python

    from contextmenu.options import CustomModelAdmin


    @admin.register(ExampleModel)
    class ExampleAdmin(CustomModelAdmin):

        def get_contextmenu_items(self, obj):
            return [
                {'title': 'Example link title', 'url': 'http://example.url'},
                .
                .
                .
                .
                {'title': 'Example link title', 'url': 'http://example.url'},
            ]
```