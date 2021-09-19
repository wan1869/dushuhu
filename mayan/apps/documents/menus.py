from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Menu

from .icons import icon_menu_documents

menu_documents = Menu(
    icon_class=icon_menu_documents, label=_('Documents Management'),
    name='documents'
)

#客户化代码 新增菜单menu_docadmin
menu_docadmin = Menu(
    icon_class=icon_menu_documents, label=_('documents quickaccess'),
    name='docadmin'
)