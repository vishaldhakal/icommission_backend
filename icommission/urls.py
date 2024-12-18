from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("affiliate.urls")),
    path("api/", include("blog.urls")),
    path("api/",include("application.urls")),
    path("api/", include("accounts.urls")),
    path('api/', include('partner.urls')),
    path('api/', include('deals.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
