from django.contrib import admin
from django.urls import path, include
from academia import views

handler404 = 'academia.views.error_404'
handler500 = 'academia.views.error_500'
handler403 = 'academia.views.error_403'
handler400 = 'academia.views.error_400'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', views.index, name="index"),
    path(r'autenticar/', include('django.contrib.auth.urls')),
    path(r'academia/', include('academia.urls')),
]