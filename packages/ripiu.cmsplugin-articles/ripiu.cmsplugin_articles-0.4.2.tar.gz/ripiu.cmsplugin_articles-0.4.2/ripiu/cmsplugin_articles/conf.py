from appconf import AppConf
from django.conf import settings  # NOQA


class CmspluginArticlesAppConf(AppConf):
    MODULE_NAME = 'Ri+'
    HEAD_CHILD_CLASSES = None
    MAIN_CHILD_CLASSES = None
    CLASSNAME = 'ripiu'
    TEMPLATES = []

    class Meta:
        prefix = 'ripiu_articles'
