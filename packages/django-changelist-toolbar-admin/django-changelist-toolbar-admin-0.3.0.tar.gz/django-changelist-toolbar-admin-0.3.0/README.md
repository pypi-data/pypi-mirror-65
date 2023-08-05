# django-changelist-toolbar-admin

Provides custom button management function on changelist page of django admin site.

## Install

```shell
pip install django-changelist-toolbar-admin
```

## Usage

**pro/settings.py**

```python
INSTALLED_APPS = [
    ...
    'django_static_fontawesome',
    'django_changelist_toolbar_admin',
    ...
]
```

- django_static_fontawesome is required, for already include the fontawesome css in Media's css settings.

**app/admin.py**

```python
from django.contrib import admin
from changelist_toolbar.admin import DjangoChangelistToolbarAdmin
from .models import Category


class CategoryAdmin(DjangoChangelistToolbarAdmin, admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

    changelist_toolbar_buttons = [
        "export",
        "say_hi",
    ]

    def export(self, request):
        return "/export"
    export.title = "Export"
    export.icon = "fas fa-file-export"
    export.target = "_blank"
    
    def say_hi(self, request):
        return {
            "href": "javascript:alert('hi');",
            "title": "Say Hi",
            "icon": "fas fa-music",
        } 

admin.site.register(Category, CategoryAdmin)
```

- Another way is override `make_changelist_toolbar_button` get return the final buttons.

## Releases

### v0.3.0 2020/04/02

- The main class rename to DjangoChangelistToolbarAdmin. Mixin is a very simple abstract class that provides helper functions, but DjangoChangelistToolbarAdmin is complex base admin, so we remove the mixin suffix.

### v0.2.0 2020/02/26

- App rename to django_changelist_toolbar_admin.

### v0.1.0 2020/02/13

- First release.
