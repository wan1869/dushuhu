from django.utils.translation import ugettext_lazy as _

from mayan.apps.document_states.classes import WorkflowAction
from mayan.apps.documents.models import (
    DocumentType, Document, DocumentVersion
)
from django.shortcuts import get_object_or_404


class TrashDocumentAction(WorkflowAction):
    label = _('Send document to trash')

    def execute(self, context):
        context['document'].delete()

#客户化 新版本上传 state action
class NewDocumentVersionAction(WorkflowAction):
    label = _('Upload as new version')

    def execute(self, context):
        document_id = context['document'].description
        # document = Document.objects.get(id=document_id)
        document = get_object_or_404(klass=Document, pk=document_id)
        file_object = context['document'].latest_version.file
        document.new_version(
            file_object=file_object, _user=None,
        )