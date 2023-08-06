
from django.apps import apps
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from cap.decorators import short_description, template_list_item

from categories.models import Category
from categories import config


def get_admin_base_class():

    if apps.is_installed('modeltranslation'):
        from modeltranslation.admin import TranslationAdmin
        return TranslationAdmin

    return admin.ModelAdmin


def get_list_display_items():

    result = ['name', 'product_count']

    if config.IS_CATEGORY_LOGO_ENABLED:
        result += ['get_preview']

    return result


def get_formfield_overrides():

    if apps.is_installed('ckeditor'):
        from ckeditor.widgets import CKEditorWidget
        return {
            models.TextField: {'widget': CKEditorWidget}
        }

    return {}


@admin.register(Category)
class CategoryAdmin(get_admin_base_class()):

    list_display = get_list_display_items()

    formfield_overrides = get_formfield_overrides()

    @template_list_item('admin/list_item_preview.html', _('Preview'))
    def get_preview(self, item):
        return {'file': item.logo}

    @short_description(_('Product count'))
    def product_count(self, item):
        return item.products.count()
