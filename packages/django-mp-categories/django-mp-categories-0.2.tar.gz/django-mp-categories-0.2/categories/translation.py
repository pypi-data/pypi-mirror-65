
from modeltranslation.translator import translator

from categories.models import Category
from categories import config


def get_fields():

    fields = ['name']

    if config.IS_CATEGORY_DESCRIPTION_ENABLED:
        fields += ['description']

    return fields


translator.register(Category, fields=get_fields())
