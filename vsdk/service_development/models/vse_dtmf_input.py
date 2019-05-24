from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from .vs_element import VoiceServiceElement
from .user_input import UserInputCategory
from vsdk.service_development.models import VoiceLabel

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
    
    repeat_recording_to_caller = models.BooleanField(_('Repeat the input to the caller before asking for confirmation'), default=True)
    repeat_voice_label = models.ForeignKey(
        VoiceLabel,
        verbose_name = _('Repeat input voice label'),
        help_text = _('The voice label that is played after the system repeats the user input. Example: "...dollars per bag of seeds."'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dtfm_repeat_voice_label'
    )
    ask_confirmation = models.BooleanField(
        _('Ask the caller to confirm their input'), default=True)
    ask_confirmation_voice_label = models.ForeignKey(
        VoiceLabel,
        verbose_name = _('Ask for confirmation voice label'),
        help_text = _('The voice label that asks the user to confirm their input. Example: "Are you satisfied with your input? Press 1 to confirm, or press 2 to retry."'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dtfm_confirmation_voice_label',
    )
    final_voice_label = models.ForeignKey(
        VoiceLabel,
        verbose_name = _('Final voice label'),
        help_text = _('The voice label that is played when the user has completed the input process. Example: "Thank you for your message! The input has been stored successfully."'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dtfm_final_voice_label',
    )

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