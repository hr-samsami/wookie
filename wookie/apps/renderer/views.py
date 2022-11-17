from rest_framework.response import Response
from rest_framework.views import APIView
from wookie.negotiation import CustomContentNegotiation


class RendererView(APIView):
    content_negotiation_class = CustomContentNegotiation

    def get(self, request):
        return Response('ok')
