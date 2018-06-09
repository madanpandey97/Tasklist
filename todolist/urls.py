from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('', include('lists.urls')),
    path('auth/', include('accounts.urls')),
    path('admin/', admin.site.urls),
]
