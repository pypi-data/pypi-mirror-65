# -*- coding: utf-8 -*-

'''
djcorecap/urls
--------------

urls for the djcorecap app
'''


from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.static import serve


allauth_templates = [
    # template, name
    ('account_inactive.html', 'account_inactive'),
    ('base.html', 'account_base'),
    ('email_confirm.html', 'account_email_verification_sent'),
    ('email.html', 'account_email'),
    ('login.html', 'account_login'),
    ('logout.html', 'account_logout'),
    ('password_change.html', 'account_change_password'),
    ('password_reset_done.html', 'account_reset_password_done'),
    ('password_reset_from_key_done.html',
     'account_reset_password_from_key_done'),
    ('password_reset_from_key.html', 'account_reset_password_from_key'),
    ('password_reset.html', 'account_reset_password'),
    ('password_set.html', 'account_set_password'),
    ('signup_closed.html', 'account_signup_closed'),
    ('signup.html', 'account_signup'),
    ('verification_sent.html', 'account_verification_email_sent'),
    ('verification_email_required.html',
     'account_verification_email_required'),
]


urlpatterns = [

    # allauth templates
    *[
        url(
            regex=(r'^account/%s/$' % n),
            view=TemplateView.as_view(
                template_name=('account/%s' % t),
            ),
            name=('%s' % n),
        ) for t, n in allauth_templates
    ],

    # base template
    url(
        regex=r'base/$',
        view=TemplateView.as_view(template_name='djcorecap/base.html'),
        name='base',
    ),

    # test template
    url(
        regex=r'test/$',
        view=TemplateView.as_view(template_name='djcorecap/test.html'),
        name='test',
    ),

    # dummy urls expected by base template
    url(
        regex=r'about/$',
        view=TemplateView.as_view(template_name='djcorecap/test.html'),
        name='about',
    ),
    url(
        regex=r'^$',
        view=TemplateView.as_view(template_name='djcorecap/test.html'),
        name='home',
    ),
]
