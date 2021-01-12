from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('search.urls')),
    path('', include('users.urls')),
    path('', include('products.urls')),
    path('', include('favorites.urls')),
]
