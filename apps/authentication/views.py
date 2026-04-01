from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import EmailTokenObtainSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse


class EmailTokenObtainView(APIView):
    @extend_schema(
        request=EmailTokenObtainSerializer,
        responses={
            200: OpenApiResponse(description='Token obtenido exitosamente'),
            400: OpenApiResponse(description='Error de validación'),
        }
    )

    def post(self, request):
        serializer= EmailTokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)