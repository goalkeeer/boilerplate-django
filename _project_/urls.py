from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include


@login_required
def index(request):
    from django.shortcuts import redirect
    return redirect(settings.INDEX_STAFF_REDIRECT_URL)


admin.site.enable_nav_sidebar = False


urlpatterns = [  # noqa: pylint=invalid-name
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('status/', include('health_check.urls')),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)

if settings.DEBUG:
    import debug_toolbar  # noqa

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
