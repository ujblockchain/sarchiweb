from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.admin.models import LogEntry
from django.views.generic import RedirectView
from project.settings.utils.otp import CustomAdminLoginView
from project.settings import env

ADMIN_PATH = env.get('ADMIN_PATH')


urlpatterns = [
    path(f'{ADMIN_PATH}/login/', CustomAdminLoginView.as_view(), name='admin_login'),
    path(f'{ADMIN_PATH}/', admin.site.urls),
    path('', include('pages.urls')),
    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon/favicon.ico')),
]

# add admin path to urlpatterns
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# inherit from the existing admin site class
class OTPAdminSite(admin.site.__class__):
    def get_log_entries(self, request):
        return LogEntry.objects.all().order_by('-action_time')


# enforce 2fa.
admin.site.__class__ = OTPAdminSite
# overrides the default 400, 404, 403 and 500 handler
handler400 = 'project.settings.utils.views.bad_request'
handler403 = 'project.settings.utils.views.permission_denied'
handler404 = 'project.settings.utils.views.page_not_found'
handler500 = 'project.settings.utils.views.server_error'
