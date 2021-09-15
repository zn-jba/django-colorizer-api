from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import HSVColor


class ModifyColorView(APIView):
    def post(self, request: Request):
        data = request.data

        if (operation := data["operation"]) not in HSVColor.HSV_OPERATIONS:
            pass

        color = HSVColor(representation=data["representation"],
                         h_value=data["color"][0],
                         s_value=data["color"][1],
                         v_value=data["color"][2],
                         operation=operation,
                         amount=data["amount"])
        original_h = color.h_value
        original_s = color.s_value
        original_v = color.v_value

        color.operate(operation)

        modified_data = {
            "representation": color.representation,
            "color": [
                original_h,
                original_s,
                original_v,
            ],
            "operation": color.operation,
            "modified_color": [
                color.h_value,
                color.s_value,
                color.v_value,
            ]
        }

        return Response(modified_data)
