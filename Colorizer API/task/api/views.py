from django.http.response import JsonResponse

from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from .colors.utility import ColorConverter
from .colors.utility import ColorModifier
from .colors.utility import ColorValidator

from .models import ColorOperation
from .serializers import ColorOperationSerializer


class ColorOperationsView(APIView):
    @staticmethod
    def get(request: Request) -> JsonResponse:
        operation = ColorOperation.objects.all()
        countries_serializer = ColorOperationSerializer(operation, many=True)
        return JsonResponse(countries_serializer.data, safe=False)

    @staticmethod
    def post(request: Request) -> JsonResponse:
        operation_data = JSONParser().parse(request)
        operation_serializer = ColorOperationSerializer(data=operation_data)
        if operation_serializer.is_valid():
            operation_serializer.save()
            return JsonResponse(operation_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(operation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ColorConversionView(APIView):
    @staticmethod
    def is_request_data_valid(data: dict) -> bool:
        representation = data.get("representation", None)
        if not representation or representation not in ColorConverter.COLOR_SPACE_MODELS:
            return False

        color = data.get("color", None)
        if not color:
            return False

        conversion = data.get("conversion", None)
        if not conversion or conversion not in ColorConverter.COLOR_SPACE_MODELS:
            return False

        if not ColorValidator.is_color_valid(representation, color):
            return False

        return True

    def post(self, request: Request) -> Response:
        if not self.is_request_data_valid(request.data):
            return Response({"error": "Invalid data."},
                            status=status.HTTP_400_BAD_REQUEST)

        representation = request.data.get("representation", None)
        color = request.data.get("color", None)
        conversion = request.data.get("conversion", None)

        context = {
            "color": color,
            "converted_color": ColorConverter.convert(representation, conversion, color)
        }

        return Response(context, status=status.HTTP_200_OK)


class ColorHarmonyView(APIView):
    @staticmethod
    def is_request_data_valid(data: dict) -> bool:
        representation = data.get("representation", None)
        if not representation or representation != "hsv":
            return False

        harmony = data.get("harmony", None)
        if not harmony or harmony != "monochromatic":
            return False

        color = data.get("color", None)
        if not color:
            return False

        if not ColorValidator.is_color_valid(representation, color):
            return False

        return True

    def post(self, request: Request) -> Response:
        if not self.is_request_data_valid(request.data):
            return Response({"error": "Invalid data."},
                            status=status.HTTP_400_BAD_REQUEST)

        representation = request.data.get("representation")
        color = request.data.get("color")

        hsv_value = color[-1]
        base = hsv_value - 40 if hsv_value >= 40 else 0
        shade = base + 20
        tint = shade + 20

        context = {
            "representation": representation,
        }

        values = [base, shade, tint]
        for index, value in enumerate(values):
            context[f"color_{index + 1}"] = [color[0], color[1], value]

        return Response(context, status=status.HTTP_200_OK)


class ModifyColorView(APIView):
    @staticmethod
    def is_request_data_valid(data: dict) -> bool:
        representation = data.get("representation")
        if not representation or representation not in ColorConverter.COLOR_SPACE_MODELS:
            return False

        operation = data.get("operation", None)
        if not operation or operation not in ColorModifier.HSV_OPERATIONS:
            return False

        color = data.get("color", None)
        if not color:
            return False

        if not ColorValidator.is_color_valid(representation, color):
            return False

        return True

    def post(self, request: Request) -> Response:
        if not self.is_request_data_valid(request.data):
            return Response({"error": "Invalid data."},
                            status=status.HTTP_400_BAD_REQUEST)

        representation = request.data.get("representation")
        color = request.data.get("color")
        operation = request.data.get("operation")
        amount = request.data.get("amount")

        modified = ColorModifier.modify(representation, operation, amount, color)

        context = {
            "representation": representation,
            "color": color,
            "operation": operation,
            "modified_color": modified
        }

        return Response(context, status=status.HTTP_200_OK)
