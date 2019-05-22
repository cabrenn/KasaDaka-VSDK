from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from .vs_element import VoiceServiceElement
from .user_input import UserInputCategory

class DtmfInput(VoiceServiceElement):
    _urls_name = 'service-development:dtmfinput'
    _redirect = models.ForeignKey(
            VoiceServiceElement,
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            related_name='%(app_label)s_%(class)s_related',
            verbose_name=_('Redirect element'),
            help_text = _("The element to redirect to after the DTMF has been validated"))
    
    input_category = models.ForeignKey(
        UserInputCategory,
        verbose_name = _('Input category'),
        help_text = _('The category under which the input will be stored in the system.'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dtmf_input_category',
    )

    @property
    def redirect(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        if self._redirect:
            return VoiceServiceElement.objects.get_subclass(id=self._redirect.id)
        else:
            return None

    class Meta:
        verbose_name = _('DTMF Element')

    def __str__(self):
        return self.name

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True
    is_valid.short_description = _('Is valid')

    def validator(self):
        errors = []
        errors.extend(super(DtmfInput, self).validator())

        if not self._redirect:
            errors.append(ugettext('DTMF Input %s does not have a redirect element') % self.name)
        return errors