from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    # admin path
    path(f'{settings.ADMIN_PATH}/', admin.site.urls),
    # apps path
    path('', include('pages.urls')),
    path('account/', include('account.urls')),
    path('blog/', include('blog.urls')),
    path('bootcamp/', include('bootcamps.urls')),
    path('contact', include('contact.urls')),
    path('newsletter', include('newsletters.urls')),
]


# add admin path to urlpatterns
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
