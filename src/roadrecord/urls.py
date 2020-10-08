from django.contrib import admin
from django.urls import path, include
from rest_auth.views import LoginView, LogoutView

from apps.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path("partner/", partner_list_create, name='partner-list'),
    path("partner/<int:pk>/", partner_detail_delete, name='partner-detail'),

    path("auto/", auto_list_create, name='auto-list'),
    path("auto/<int:pk>/", auto_detail_delete, name='auto-detail'),

    # path("autopartner/", autopartnerkapcsolat_list, name='kapcsolat-detail'),
    # path("autopartner/<int:pk>/", autopartnerkapcsolat_detail_delete, name='kapcsolat-detail'),

]
