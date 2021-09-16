from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from .models.colors import HSVColor

from .models import ColorOperation
from .serializers import ColorOperationSerializer


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

    # def put(self, request: Request):
    #     pass
    #
    # def patch(self, request: Request):
    #     pass
    #
    # def delete(self, request: Request):
    #     pass


class ModifyColorView(APIView):
    # def get(self, request: Request, format=None):
    #     colors = HSVColor.objects.all()
    #     serializer = HSVColorSerializer(colors, many=True)
    #     return Response(serializer.data)

    def post(self, request: Request):
        if (operation := request.data.get("operation", None)) not in HSVColor.HSV_OPERATIONS:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        color = HSVColor(request.data)
        modified_data = color.operate(operation, commit=True)

        return Response(modified_data, status=status.HTTP_200_OK)
