from django.test import override_settings

from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..permissions import (
    permission_document_type_file_metadata_setup,
    permission_file_metadata_submit, permission_file_metadata_view
)

from .literals import TEST_FILE_METADATA_KEY
from .mixins import DocumentTypeViewsTestMixin, FileMetadataViewsTestMixin


class DocumentTypeViewsTestCase(
    DocumentTypeViewsTestMixin, GenericDocumentViewTestCase
):
    def test_document_type_settings_view_no_permission(self):
        response = self._request_document_type_settings_view()
        self.assertEqual(response.status_code, 404)

    def test_document_type_settings_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_file_metadata_setup
        )

        response = self._request_document_type_settings_view()
        self.assertEqual(response.status_code, 200)

    def test_document_type_submit_view_no_permission(self):
        response = self._request_document_type_submit_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_document.latest_version.file_metadata_drivers.count(), 0
        )

    def test_document_type_submit_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type, permission=permission_file_metadata_submit
        )

        response = self._request_document_type_submit_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.latest_version.file_metadata_drivers.count(), 1
        )


@override_settings(FILE_METADATA_AUTO_PROCESS=True)
class FileMetadataViewsTestCase(
    FileMetadataViewsTestMixin, GenericDocumentViewTestCase
):
    def setUp(self):
        super(FileMetadataViewsTestCase, self).setUp()
        self.test_driver = self.test_document.latest_version.file_metadata_drivers.first()

    def test_document_version_driver_list_view_no_permission(self):
        response = self._request_document_version_driver_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_version_driver_list_view_with_access(self):
        self.grant_access(
            permission=permission_file_metadata_view, obj=self.test_document
        )

        response = self._request_document_version_driver_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )

    def test_document_version_file_metadata_list_view_no_permission(self):
        response = self._request_document_version_file_metadata_list_view()
        self.assertNotContains(
            response=response, text=TEST_FILE_METADATA_KEY, status_code=404
        )

    def test_document_version_file_metadata_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_file_metadata_view
        )

        response = self._request_document_version_file_metadata_list_view()
        self.assertContains(
            response=response, text=TEST_FILE_METADATA_KEY, status_code=200
        )

    def test_document_submit_view_no_permission(self):
        self.test_document.latest_version.file_metadata_drivers.all().delete()

        response = self._request_document_submit_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.latest_version.file_metadata_drivers.count(), 0
        )

    def test_document_submit_view_with_access(self):
        self.test_document.latest_version.file_metadata_drivers.all().delete()
        self.grant_access(
            permission=permission_file_metadata_submit, obj=self.test_document
        )

        response = self._request_document_submit_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.latest_version.file_metadata_drivers.count(), 1
        )

    def test_multiple_document_submit_view_no_permission(self):
        self.test_document.latest_version.file_metadata_drivers.all().delete()

        response = self._request_multiple_document_submit_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.latest_version.file_metadata_drivers.count(), 0
        )

    def test_multiple_document_submit_view_with_access(self):
        self.test_document.latest_version.file_metadata_drivers.all().delete()
        self.grant_access(
            permission=permission_file_metadata_submit, obj=self.test_document
        )

        response = self._request_multiple_document_submit_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.latest_version.file_metadata_drivers.count(), 1
        )
