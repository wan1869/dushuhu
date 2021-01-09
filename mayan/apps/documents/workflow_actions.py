from django.utils.translation import ugettext_lazy as _

from mayan.apps.document_states.classes import WorkflowAction
from mayan.apps.documents.models import Document
from django.shortcuts import get_object_or_404

from mayan.apps.metadata.models import DocumentMetadata

class TrashDocumentAction(WorkflowAction):
    label = _('Send document to trash')

    def execute(self, context):
        context['document'].delete()

#客户化 新版本上传 state action
class NewDocumentVersionAction(WorkflowAction):
    label = _('Upload as new version')

    def execute(self, context):
        document_uuid = context['document'].description
        document_id = context['document'].pk
        # document = Document.objects.get(id=document_id)
        document = get_object_or_404(klass=Document, uuid=document_uuid)
        #copy metadata
        metadata = DocumentMetadata.objects.filter(metadata_type__name="creator", document_id=document_id)
        creator_name = metadata[0].value
        result = DocumentMetadata.objects.filter(metadata_type__name="creator", document_id=document.id)
        result.update(value=creator_name)
        metadata1 = DocumentMetadata.objects.filter(metadata_type__name="reviewer", document_id=document_id)
        reviewer_name = metadata1[0].value
        result1 = DocumentMetadata.objects.filter(metadata_type__name="reviewer", document_id=document.id)
        result1.update(value=reviewer_name)
        metadata2 = DocumentMetadata.objects.filter(metadata_type__name="approver", document_id=document_id)
        approver_name = metadata2[0].value
        result2 = DocumentMetadata.objects.filter(metadata_type__name="approver", document_id=document.id)
        result2.update(value=approver_name)
        metadata3 = DocumentMetadata.objects.filter(metadata_type__name="effective_date", document_id=document_id)
        effective_date = metadata3[0].value
        result3 = DocumentMetadata.objects.filter(metadata_type__name="effective_date", document_id=document.id)
        result3.update(value=effective_date)
        #new version
        file_object = context['document'].latest_version.file
        document.new_version(
            file_object=file_object, _user=None,
        )
