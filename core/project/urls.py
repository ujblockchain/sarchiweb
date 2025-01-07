from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # admin path
    path(f'{settings.ADMIN_PATH}/', admin.site.urls),
    # apps path
    path('', include('core.pages.urls')),
    path('account/', include('core.account.urls')),
    path('blog/', include('core.blog.urls')),
    path('bootcamp/', include('core.bootcamps.urls')),
    path('masterclass/', include('core.masterclass.urls')),
    path('contact/', include('core.contact.urls')),
    path('newsletter/', include('core.newsletters.urls')),
    path('event/', include('core.program.urls')),
]

# add admin path to urlpatterns
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
