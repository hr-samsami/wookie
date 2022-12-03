from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from wookie.negotiation import CustomContentNegotiation

header_param = openapi.Parameter('Content-Type', openapi.IN_HEADER,
                                 description="Content-Type of header param.\n"
                                             "Use `application/xml` for xml response "
                                             "or `application/json` for json response.",
                                 type=openapi.IN_HEADER)


class RendererView(APIView):
    content_negotiation_class = CustomContentNegotiation
    permission_classes = [AllowAny]

    @swagger_auto_schema(manual_parameters=[header_param])
    def get(self, request):
        return Response('ok')

    @swagger_auto_schema(manual_parameters=[header_param])
    def post(self, request):
        return Response('ok')
