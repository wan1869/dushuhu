from django.conf.urls import url

from .api_views import (
    APIStagingSourceFileView, APIStagingSourceFileImageView,
    APIStagingSourceFileUploadView, APIStagingSourceListView,
    APIStagingSourceView
)
from .views import (
    SourceCheckView, SourceCreateView, SourceDeleteView,
    SourceEditView, SourceListView, StagingFileDeleteView,
    DocumentVersionUploadInteractiveView, UploadInteractiveView,UploadNewVersionInteractiveView,UploadModifyApplicationInteractiveView
)
from .wizards import DocumentCreateWizard
# 客户化代码 新增版本菜单的wizard视图
from .customwizards import DocumentVersionCreateWizard

# 客户化代码 文档修改菜单的wizard视图
from .customwizards import DocumentModifyApplicationWizard

urlpatterns = [
    url(
        regex=r'^staging_folders/(?P<staging_folder_id>\d+)/files/(?P<encoded_filename>.+)/delete/$',
        name='staging_file_delete', view=StagingFileDeleteView.as_view()
    ),

    # Document create views

    url(
        regex=r'^documents/create/from/local/multiple/$',
        name='document_create_multiple', view=DocumentCreateWizard.as_view()
    ),
    # 客户化代码 菜单"新增版本"链接
    url(
        regex=r'^documents/version/create/from/local/multiple/$',
        name='document_version_create_multiple', view=DocumentVersionCreateWizard.as_view()
    ),
    # 客户化代码 菜单"文档修改申请"链接
    url(
        regex=r'^documents/modify/from/local/multiple/$',
        name='document_modify_application', view=DocumentModifyApplicationWizard.as_view()
    ),
    url(
        regex=r'^documents/upload/new/interactive/(?P<source_id>\d+)/$',
        name='document_upload_interactive',
        view=UploadInteractiveView.as_view()
    ),
    url(
        regex=r'^documents/upload/new/interactive/$',
        name='document_upload_interactive',
        view=UploadInteractiveView.as_view()
    ),
    # 客户化代码 跳转文件新版本上传视图
    url(
        regex=r'^documents/upload/new/version/interactive/$',
        name='document_upload_new_version',
        view=UploadNewVersionInteractiveView.as_view()
    ),
    # 客户化代码 跳转文档修改申请视图
    url(
        regex=r'^documents/upload/modify/application/interactive/$',
        name='document_upload_modify_application',
        view=UploadModifyApplicationInteractiveView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/versions/upload/interactive/(?P<source_id>\d+)/$',
        name='document_version_upload',
        view=DocumentVersionUploadInteractiveView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/versions/upload/interactive/$',
        name='document_version_upload',
        view=DocumentVersionUploadInteractiveView.as_view()
    ),
    #客户化方法
    url(
        regex=r'^documents/upload/new/interactive/(?P<versioned_document_id>\d+)/$',
        name='document_upload_new_version_document',
        view=UploadNewVersionInteractiveView.as_view()
    ),
    #客户化方法
    url(
        regex=r'^documents/upload/modify/interactive/(?P<versioned_document_id>\d+)/$',
        name='document_upload_modify_document',
        view=UploadModifyApplicationInteractiveView.as_view()
    ),

    # Setup views

    url(
        regex=r'^sources/$', name='setup_source_list',
        view=SourceListView.as_view()
    ),
    url(
        regex=r'^sources/create/(?P<source_type_name>\w+)/$',
        name='setup_source_create', view=SourceCreateView.as_view()
    ),
    url(
        regex=r'^sources/(?P<source_id>\d+)/check/$',
        name='setup_source_check', view=SourceCheckView.as_view()
    ),
    url(
        regex=r'^sources/(?P<source_id>\d+)/delete/$',
        name='setup_source_delete', view=SourceDeleteView.as_view()
    ),
    url(
        regex=r'^sources/(?P<source_id>\d+)/edit/$', name='setup_source_edit',
        view=SourceEditView.as_view()
    ),
]

api_urls = [
    url(
        regex=r'^staging_folders/file/(?P<staging_folder_pk>[0-9]+)/(?P<encoded_filename>.+)/image/$',
        name='stagingfolderfile-image',
        view=APIStagingSourceFileImageView.as_view()
    ),
    url(
        regex=r'^staging_folders/file/(?P<staging_folder_pk>[0-9]+)/(?P<encoded_filename>.+)/upload/$',
        name='stagingfolderfile-upload',
        view=APIStagingSourceFileUploadView.as_view()
    ),
    url(
        regex=r'^staging_folders/file/(?P<staging_folder_pk>[0-9]+)/(?P<encoded_filename>.+)/$',
        name='stagingfolderfile-detail',
        view=APIStagingSourceFileView.as_view()
    ),
    url(
        regex=r'^staging_folders/$', name='stagingfolder-list',
        view=APIStagingSourceListView.as_view()
    ),
    url(
        regex=r'^staging_folders/(?P<pk>[0-9]+)/$',
        name='stagingfolder-detail', view=APIStagingSourceView.as_view()
    )
]
