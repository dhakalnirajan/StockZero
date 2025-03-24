from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/chess/', include('webapp.chessgame.urls')),
    path('', include('webapp.frontend.urls')),
]