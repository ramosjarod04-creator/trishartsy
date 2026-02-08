from django.contrib import admin
from django.urls import path, include
from booking import views  # import views to use home_redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_redirect, name='home'),  # redirects root to login
    path('admin/', admin.site.urls),
    path('', include('booking.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)