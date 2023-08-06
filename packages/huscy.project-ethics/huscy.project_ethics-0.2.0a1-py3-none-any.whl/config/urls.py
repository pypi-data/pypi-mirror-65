from django.contrib import admin
from django.urls import include, path

from huscy.project_ethics.urls import router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
]
