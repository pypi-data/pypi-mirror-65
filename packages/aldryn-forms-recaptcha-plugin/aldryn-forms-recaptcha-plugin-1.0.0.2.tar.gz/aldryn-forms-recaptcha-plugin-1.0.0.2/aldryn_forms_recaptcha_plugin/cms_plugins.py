from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool
from aldryn_forms.cms_plugins import Field
from snowpenguin.django.recaptcha3.fields import ReCaptchaField
from snowpenguin.django.recaptcha3.widgets import ReCaptchaHiddenInput


class ReCaptchaFieldPlugin(Field):
    name = _("Invisible ReCaptcha Field")
    render_template = True
    allow_children = False
    form_field = ReCaptchaField
    form_field_widget = ReCaptchaHiddenInput

    form_field_enabled_options = [
        'error_messages',
    ]
    fieldset_general_fields = []
    fieldset_advanced_fields = []

    def get_error_messages(self, instance) -> dict:
        return {
            'required': _(
                "There was a problem with ReCaptcha V3. "
                "Please contact support if this problem persists."
            ),
        }


plugin_pool.register_plugin(ReCaptchaFieldPlugin)
