# -*- coding: utf-8 -*-
from plone.app.users.browser.register import RegistrationForm as BaseForm
from zope.interface import Interface
from quintagroup.formlib.captcha import Captcha
from quintagroup.formlib.captcha import CaptchaWidget
from zope.formlib import form
from plone import api
from Products.CMFPlone import PloneMessageFactory as _


class ICCPDCaptchaSchema(Interface):
    """ """

    captcha = Captcha(
        title=u'Codice di verifica',
        description=u'Inserisci il codice di verifica che vedi.',
    )


class RegistrationForm(BaseForm):
    """
    """

    @property
    def form_fields(self):
        fields = super(RegistrationForm, self).form_fields
        fields += form.Fields(ICCPDCaptchaSchema)
        fields['captcha'].custom_widget = CaptchaWidget

        return fields

    @form.action(
        _(u'label_register', default=u'Register'),
        validator='validate_registration',
        name=u'register',
    )
    def action_join(self, action, data):
        self.handle_join_success(data)

        # XXX Return somewhere else, depending on what
        # handle_join_success returns?
        api.portal.show_message(
            message='Utente iscritto correttamente. Prima di poter accedere, controlla la tua casella email per confermare l\'attivazione.',  # noqa
            request=self.request,
        )
        came_from = self.request.form.get('came_from')
        if came_from:
            utool = api.portal.get_tool(name='portal_url')
            if utool.isURLInPortal(came_from):
                self.request.response.redirect(came_from)
                return ''
        return self.context.unrestrictedTraverse('registered')()
