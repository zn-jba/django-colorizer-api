from django.urls import path

from .views import ModifyColorView

app_name = "api"

urlpatterns = [
    path("modify-color/", ModifyColorView.as_view(), name="modify-color"),
]
