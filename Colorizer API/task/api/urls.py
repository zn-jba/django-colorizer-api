from django.urls import path

from .views import ColorOperationsView
from .views import ColorConversionView
from .views import ModifyColorView

app_name = "api"

urlpatterns = [
    path("convert-color/", ColorConversionView.as_view(), name="convert-color"),
    path("modify-color/", ModifyColorView.as_view(), name="modify-color"),

    # Experimentation
    path("api/operations/", ColorOperationsView.as_view(), name="operation"),
]
