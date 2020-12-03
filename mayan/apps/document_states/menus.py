from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Menu

from .icons import icon_workflow

menu_workflow = Menu(
    icon_class=icon_workflow, label=_('Workflow'),
    name='workflows'
)
