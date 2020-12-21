from django.apps import apps
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.dashboards.classes import DashboardWidgetNumeric

from .icons import icon_workflow_runtime_proxy_list
from .permissions import permission_workflow_view


class DashboardWidgetWaitingWorkflows(DashboardWidgetNumeric):
    icon_class = icon_workflow_runtime_proxy_list
    label = _('All Workflows')
    link = reverse_lazy(viewname='document_states:workflow_list_waiting_approval')

    def render(self, request):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )
        Proxy = apps.get_model(
            app_label='document_states', model_name='WorkflowWaitingProxy'
        )

        self.count = AccessControlList.objects.restrict_queryset(
            permission=permission_workflow_view, user=request.user,
            queryset=Proxy.objects.all()
        ).count()
        return super(DashboardWidgetWaitingWorkflows, self).render(request)
