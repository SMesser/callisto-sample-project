# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from callisto.delivery.views import (
    delete_report, edit_record_form_view, export_as_pdf, new_record_form_view,
    submit_to_matching, submit_to_school, withdraw_from_matching,
)

from callisto_sample_project.core.forms import (
    CustomMatchReport, CustomReport, EncryptedFormWizard,
)

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),

    # User management
    url(r'^users/', include('callisto_sample_project.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    # Callisto core views
    url(r'^reports/new/(?P<step>.+)/$', new_record_form_view,
        {'wizard': EncryptedFormWizard,
         'url_name': 'test_new_report'}, name="test_new_report"),
    url(r'^reports/edit/(?P<edit_id>\d+)/$', edit_record_form_view,
        {'wizard': EncryptedFormWizard, 'url_name': 'test_edit_report'}, name='test_edit_report'),
    url(r'^reports/edit/(?P<edit_id>\d+)/(?P<step>.+)/$', edit_record_form_view,
        {'wizard': EncryptedFormWizard, 'url_name': 'test_edit_report'}, name='test_edit_report'),
    url(r'^reports/submit/(?P<report_id>\d+)/$', submit_to_school, name="test_submit_report"),
    url(r'^reports/submit_custom/(?P<report_id>\d+)/$', submit_to_school,
        {'form_template_name': 'submit_to_school_custom.html',
         'confirmation_template_name': 'submit_to_school_confirmation_custom.html',
         'report_class': CustomReport,
         'extra_context': {'test': 'custom context'}}, name="test_submit_confirmation"),
    url(r'^reports/match/(?P<report_id>\d+)/$', submit_to_matching, name="test_submit_match"),
    url(r'^reports/match_custom/(?P<report_id>\d+)/$', submit_to_matching,
        {'form_template_name': 'submit_to_matching_custom.html',
         'confirmation_template_name': 'submit_to_matching_confirmation_custom.html',
         'report_class': CustomMatchReport,
         'extra_context': {'test': 'custom context'}}, name="test_match_confirmation"),
    url(r'^reports/withdraw_match/(?P<report_id>\d+)/$', withdraw_from_matching,
        {'template_name': 'after_withdraw.html',
         'extra_context': {'test': 'custom context'}}, name="test_withdraw_match"),
    url(r'^reports/export/(?P<report_id>\d+)/$', export_as_pdf, name="test_export"),
    url(r'^reports/export_custom/(?P<report_id>\d+)/$', export_as_pdf,
        {'report_class': CustomReport,
         'extra_context': {'test': 'custom context'}}, name="test_export_custom"),
    url(r'^reports/delete/(?P<report_id>\d+)/$', delete_report,
        {'extra_context': {'test': 'custom context'}}, name="delete_report")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
