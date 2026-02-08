from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('gallery/', views.gallery_view, name='gallery'),
    path('about/', views.about_view, name='about'),
    path('book/', views.book_view, name='book'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_gallery/', views.admin_gallery, name='admin_gallery'),

    # Admin
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('accept/<int:pk>/', views.accept_booking, name='accept_booking'),
    path('deny/<int:pk>/', views.deny_booking, name='deny_booking'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)