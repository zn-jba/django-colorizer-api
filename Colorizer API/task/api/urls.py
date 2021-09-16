from django.urls import path

from .views import ModifyColorView
from .views import ColorOperationsView

app_name = "api"

urlpatterns = [
    path("api/operations/", ColorOperationsView.as_view(), name="operation"),
    path("modify-color/", ModifyColorView.as_view(), name="modify-color"),
]
