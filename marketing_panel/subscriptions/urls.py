from django.urls import path
from . import views

urlpatterns = [
    path("new_user/", views.new_user, name="new_user"),
    path("check_access/", views.check_access, name="check_access"),
]
