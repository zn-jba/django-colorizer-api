from django.http.response import JsonResponse

from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import ColorOperation
from .models.colors import HSVColor
from .serializers import ColorOperationSerializer

from .colors.utility import ColorConverter


class ColorOperationsView(APIView):
    def get(self, request: Request) -> JsonResponse:
        operation = ColorOperation.objects.all()
        countries_serializer = ColorOperationSerializer(operation, many=True)
        return JsonResponse(countries_serializer.data, safe=False)

    def post(self, request: Request) -> JsonResponse:
        operation_data = JSONParser().parse(request)
        operation_serializer = ColorOperationSerializer(data=operation_data)
        if operation_serializer.is_valid():
            operation_serializer.save()
            return JsonResponse(operation_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(operation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ColorConversionView(APIView):
    def post(self, request: Request):
        is_valid = True
        data = request.data
        representation = data.get("representation", None)
        colors = data.get("color", None)
        conversion = data.get("conversion", None)

        if not conversion:
            is_valid = False

        if request.data.get("representation", None) not in ("rgb", "hsv"):
            is_valid = False

        if is_valid and representation == "hsv":
            is_valid = ColorConverter.is_hsv_color_values_valid(colors)
        elif is_valid and representation == "rgb":
            is_valid = ColorConverter.is_rgb_color_values_valid(colors)

        if not is_valid:
            return Response({"error": "Invalid data."},
                            status=status.HTTP_400_BAD_REQUEST)

        context = {
            "color": data.get("color", ""),
        }

        if conversion == "rgb":
            rgb_colors = ColorConverter.convert_hsv_to_rgb(*colors)
            context["converted_color"] = rgb_colors
        elif conversion == "hsv":
            hsv_colors = ColorConverter.convert_rgb_to_hsv(*colors)
            context["converted_color"] = hsv_colors

        return Response(context, status=status.HTTP_200_OK)


class ModifyColorView(APIView):
    def post(self, request: Request):
        is_valid = True

        if (operation := request.data.get("operation", None)) not in HSVColor.HSV_OPERATIONS:
            is_valid = False

        if request.data.get("representation", None) not in ("rgb", "hsv"):
            is_valid = False

        if is_valid:
            colors = request.data.get("color", None)
            is_valid = ColorConverter.is_hsv_color_values_valid(colors)

        if is_valid:
            color = HSVColor(request.data)
            modified_data = color.operate(operation, commit=True)
            return Response(modified_data, status=status.HTTP_200_OK)

        return Response({"error": "Invalid data."},
                        status=status.HTTP_400_BAD_REQUEST)
