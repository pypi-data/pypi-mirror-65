
from categories import defaults


class CategorySettings(object):

    IS_CATEGORY_LOGO_ENABLED = defaults.IS_CATEGORY_LOGO_ENABLED
    IS_CATEGORY_ICON_ENABLED = defaults.IS_CATEGORY_ICON_ENABLED
    IS_CATEGORY_DESCRIPTION_ENABLED = defaults.IS_CATEGORY_DESCRIPTION_ENABLED

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + ['categories']
