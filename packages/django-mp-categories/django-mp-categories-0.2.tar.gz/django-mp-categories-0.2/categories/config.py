
from django.conf import settings

from categories import defaults


IS_CATEGORY_LOGO_ENABLED = getattr(
    settings,
    'IS_CATEGORY_LOGO_ENABLED',
    defaults.IS_CATEGORY_LOGO_ENABLED)

IS_CATEGORY_ICON_ENABLED = getattr(
    settings,
    'IS_CATEGORY_ICON_ENABLED',
    defaults.IS_CATEGORY_ICON_ENABLED)

IS_CATEGORY_DESCRIPTION_ENABLED = getattr(
    settings,
    'IS_CATEGORY_DESCRIPTION_ENABLED',
    defaults.IS_CATEGORY_DESCRIPTION_ENABLED)
