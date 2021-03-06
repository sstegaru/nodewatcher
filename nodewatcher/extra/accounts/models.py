from django.conf import settings
from django import db
from django.db import models as django_models
from django.db.models import signals as models_signals
from django.contrib.auth import models as auth_models
from django.template import loader
from django.utils.translation import ugettext_lazy as _

from registration import models as registration_models

from phonenumber_field import modelfields as phonenumber_fields

from nodewatcher.modules.administration.projects import models
from nodewatcher.utils.fields import geographic

ATTRIBUTION_CHOICES = (
    ('name', _("Use my full name")),
    ('username', _("Use my username")),
    ('nothing', _("Hide me")),
)


class UserProfileAndSettings(django_models.Model):
    """
    This class represents an user profile and settings.
    """

    user = django_models.OneToOneField(auth_models.User, editable=False)

    phone_number = phonenumber_fields.PhoneNumberField(_('phone number'), help_text=_('Please enter your phone number in international format (e.g. +38651654321) for use in emergency. It will be visible only to network administrators.'), null=True)
    country = geographic.CountryField(_('country'), blank=True, help_text=_('Where are you from? It will be public.'))
    language = geographic.LanguageField(_('language'), help_text=_('Choose the language you wish this site to be in.'))
    default_project = django_models.ForeignKey(models.Project, default=models.project_default, null=True, verbose_name=_('default project'))
    attribution = django_models.CharField(_('attribution'), max_length=8, choices=ATTRIBUTION_CHOICES, default=ATTRIBUTION_CHOICES[0][0], help_text=_('What to use when we want to give you public attribution for your participation and contribution?'))

    # AccountRegistrationForm and AccountChangeForm uses this
    fieldset = (
        (_('Additional personal info'), {
            'fields': ('phone_number', 'country'),
        }),
        (_('Settings'), {
            'fields': ('language', 'default_project'),
        }),
        (_('Privacy'), {
            'fields': ('attribution',),
        }),
    )

    class Meta:
        verbose_name = _('user profile and settings')
        verbose_name_plural = _('users profiles and settings')

    def __unicode__(self):
        return u"profile and settings for %s" % (self.user)

    @django_models.permalink
    def get_absolute_url(self):
        return ('user_account',)


def create_profile_and_settings(sender, instance, created, **kwargs):
    if created:
        try:
            # We try to create profile and settings object so that it always exist
            UserProfileAndSettings.objects.create(user=instance)
        except db.IntegrityError:
            pass

models_signals.post_save.connect(create_profile_and_settings, sender=auth_models.User)


# Monkey-patch registration_models.RegistrationProfile
def send_activation_email(instance, site, email_change=False):
    """
    Based on `registration.models.RegistrationProfile.send_activation_email` to extend activation e-mail template context with
    `email_change` boolean and other values.
    """

    protocol = 'https' if getattr(settings, 'USE_HTTPS', False) else 'http'

    ctx_dict = {
        'email': instance.user.email,
        'domain': site.domain,
        'site_name': site.name,
        'user': instance.user,
        'protocol': protocol,
        'activation_key': instance.activation_key,
        'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
        'NETWORK': getattr(settings, 'NETWORK', {}),
        'email_change': email_change,
    }
    subject = loader.render_to_string('registration/activation_email_subject.txt', ctx_dict)
    subject = ''.join(subject.splitlines())

    message = loader.render_to_string('registration/activation_email.txt', ctx_dict)

    instance.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
registration_models.RegistrationProfile.send_activation_email = send_activation_email

orig_activation_key_expired = registration_models.RegistrationProfile.activation_key_expired


def activation_key_expired(instance):
    """
    Determines whether this `RegistrationProfile`'s activation key has expired.

    For users which have already logged in activation key never expires (they have probably changed their e-mail address).
    Otherwise original `registration.models.RegistrationProfile.activation_key_expired` rules apply.
    """

    if instance.user.last_login != instance.user.date_joined:
        return False
    return orig_activation_key_expired(instance)
activation_key_expired.boolean = True
registration_models.RegistrationProfile.activation_key_expired = activation_key_expired

try:
    # So that signals are registered early on
    from . import signals
except ImportError:
    # Probably circular imports
    pass
