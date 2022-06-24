from django.urls import path, include

urlpatterns = [
    path('auth/', include('prek.api.v1.auth.urls'))
]
