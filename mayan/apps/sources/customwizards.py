from furl import furl


from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import classonlymethod
from django.utils.translation import ugettext_lazy as _

from formtools.wizard.views import SessionWizardView

from mayan.apps.documents.forms.document_forms import DocumentFilteredSelectForm
from mayan.apps.documents.permissions import permission_document_create

from .icons import icon_wizard_submit

#客户化代码 新版本上传向导页
class WizardStep:
    _deregistry = {}
    _registry = {}

    @classmethod
    def deregister(cls, step):
        cls._deregistry[step.name] = step

    @classmethod
    def deregister_all(cls):
        for step in cls.get_all():
            cls.deregister(step=step)

    @classmethod
    def done(cls, wizard):
        return {}

    @classmethod
    def get(cls, name):
        for step in cls.get_all():
            if name == step.name:
                return step

    @classmethod
    def get_all(cls):
        return sorted(
            [
                step for step in cls._registry.values() if step.name not in cls._deregistry
            ], key=lambda x: x.number
        )

    @classmethod
    def get_choices(cls, attribute_name):
        return [
            (step.name, getattr(step, attribute_name)) for step in cls.get_all()
        ]

    @classmethod
    def get_form_initial(cls, wizard):
        return {}

    @classmethod
    def get_form_kwargs(cls, wizard):
        return {}

    @classmethod
    def post_upload_process(cls, document, querystring=None):
        for step in cls.get_all():
            step.step_post_upload_process(
                document=document, querystring=querystring
            )

    @classmethod
    def register(cls, step):
        if step.name in cls._registry:
            raise Exception('A step with this name already exists: %s' % step.name)

        if step.number in [reigstered_step.number for reigstered_step in cls.get_all()]:
            raise Exception('A step with this number already exists: %s' % step.name)

        cls._registry[step.name] = step

    @classmethod
    def reregister(cls, name):
        cls._deregistry.pop(name)

    @classmethod
    def reregister_all(cls):
        cls._deregistry = {}

    @classmethod
    def step_post_upload_process(cls, document, querystring=None):
        pass

# 客户化代码 "新增版本"的第一步
class WizardStepDocument(WizardStep):
    form_class = DocumentFilteredSelectForm
    label = _('Select document')
    name = 'document_selection'
    number = 0

    @classmethod
    def condition(cls, wizard):
        return True

    # 返回选择的document_id
    @classmethod
    def done(cls, wizard):
        cleaned_data = wizard.get_cleaned_data_for_step(step=cls.name)
        if cleaned_data:
            return {
                'versioned_document_id': cleaned_data['document_id'].pk
            }

    @classmethod
    def get_form_kwargs(cls, wizard):
        return {
            'permission': permission_document_create,
            'user': wizard.request.user
        }

# 注册第一步
WizardStep.register(WizardStepDocument)


class DocumentVersionCreateWizard(SessionWizardView):
    template_name = 'appearance/generic_wizard.html'

    @classonlymethod
    def as_view(cls, *args, **kwargs):
        cls.form_list = WizardStep.get_choices(attribute_name='form_class')
        cls.condition_dict = dict(
            WizardStep.get_choices(attribute_name='condition')
        )
        return super(DocumentVersionCreateWizard, cls).as_view(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        # InteractiveSource = apps.get_model(
        #     app_label='sources', model_name='InteractiveSource'
        # )

        form_list = WizardStep.get_choices(attribute_name='form_class')
        condition_dict = dict(
            WizardStep.get_choices(attribute_name='condition')
        )

        result = self.__class__.get_initkwargs(
            condition_dict=condition_dict, form_list=form_list
        )
        self.form_list = result['form_list']
        self.condition_dict = result['condition_dict']

        # if not InteractiveSource.objects.filter(enabled=True).exists():
        #     messages.error(
        #         message=_(
        #             'No interactive document have been uploaded or '
        #             'none have been enabled, create one before proceeding.'
        #         ),
        #         request=request
        #     )
        #     return HttpResponseRedirect(
        #         redirect_to=reverse(viewname='sources:document_create_multiple')
        #     )

        return super(
            DocumentVersionCreateWizard, self
        ).dispatch(request, *args, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super(
            DocumentVersionCreateWizard, self
        ).get_context_data(form=form, **kwargs)

        wizard_step = WizardStep.get(name=self.steps.current)

        context.update(
            {
                'form_css_classes': 'form-hotkey-double-click',
                'step_title': _(
                    'Step %(step)d of %(total_steps)d: %(step_label)s'
                ) % {
                    'step': self.steps.step1, 'total_steps': len(self.form_list),
                    'step_label': wizard_step.label,
                },
                'submit_label': _('Next step'),
                'submit_icon_class': icon_wizard_submit,
                'title': _('Document upload wizard'),
                'wizard_step': wizard_step,
                'wizard_steps': WizardStep.get_all(),
            }
        )
        return context

    def get_form_initial(self, step):
        return WizardStep.get(name=step).get_form_initial(wizard=self) or {}

    def get_form_kwargs(self, step):
        return WizardStep.get(name=step).get_form_kwargs(wizard=self) or {}

    def done(self, form_list, **kwargs):
        query_dict = {}

        for step in WizardStep.get_all():
            query_dict.update(step.done(wizard=self) or {})
        # 跳转到文件上传页面
        url = furl(reverse(viewname='sources:document_upload_new_version'))
        # Use equal and not .update() to get the same result as using
        # urlencode(doseq=True)
        url.args = query_dict

        return HttpResponseRedirect(redirect_to=url.tostr())

class DocumentModifyApplicationWizard(SessionWizardView):
    template_name = 'appearance/generic_wizard.html'

    @classonlymethod
    def as_view(cls, *args, **kwargs):
        cls.form_list = WizardStep.get_choices(attribute_name='form_class')
        cls.condition_dict = dict(
            WizardStep.get_choices(attribute_name='condition')
        )
        return super(DocumentModifyApplicationWizard, cls).as_view(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        # InteractiveSource = apps.get_model(
        #     app_label='sources', model_name='InteractiveSource'
        # )

        form_list = WizardStep.get_choices(attribute_name='form_class')
        condition_dict = dict(
            WizardStep.get_choices(attribute_name='condition')
        )

        result = self.__class__.get_initkwargs(
            condition_dict=condition_dict, form_list=form_list
        )
        self.form_list = result['form_list']
        self.condition_dict = result['condition_dict']

        # if not InteractiveSource.objects.filter(enabled=True).exists():
        #     messages.error(
        #         message=_(
        #             'No interactive document have been uploaded or '
        #             'none have been enabled, create one before proceeding.'
        #         ),
        #         request=request
        #     )
        #     return HttpResponseRedirect(
        #         redirect_to=reverse(viewname='sources:document_create_multiple')
        #     )

        return super(
            DocumentModifyApplicationWizard, self
        ).dispatch(request, *args, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super(
            DocumentModifyApplicationWizard, self
        ).get_context_data(form=form, **kwargs)

        wizard_step = WizardStep.get(name=self.steps.current)

        context.update(
            {
                'form_css_classes': 'form-hotkey-double-click',
                'step_title': _(
                    'Step %(step)d of %(total_steps)d: %(step_label)s'
                ) % {
                    'step': self.steps.step1, 'total_steps': len(self.form_list),
                    'step_label': wizard_step.label,
                },
                'submit_label': _('Next step'),
                'submit_icon_class': icon_wizard_submit,
                'title': _('Document upload wizard'),
                'wizard_step': wizard_step,
                'wizard_steps': WizardStep.get_all(),
            }
        )
        return context

    def get_form_initial(self, step):
        return WizardStep.get(name=step).get_form_initial(wizard=self) or {}

    def get_form_kwargs(self, step):
        return WizardStep.get(name=step).get_form_kwargs(wizard=self) or {}

    def done(self, form_list, **kwargs):
        query_dict = {}

        for step in WizardStep.get_all():
            query_dict.update(step.done(wizard=self) or {})
        # 跳转到文件上传页面
        url = furl(reverse(viewname='sources:document_upload_modify_application'))
        # Use equal and not .update() to get the same result as using
        # urlencode(doseq=True)
        url.args = query_dict

        return HttpResponseRedirect(redirect_to=url.tostr())
