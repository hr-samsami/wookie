from rest_framework.negotiation import DefaultContentNegotiation


CONTENT_TYPES = {
    'application/json': 'json',
    'application/xml': 'xml'
}


class CustomContentNegotiation(DefaultContentNegotiation):
    def select_renderer(self, request, renderers, format_suffix=None):
        if content_type := CONTENT_TYPES.get(request.headers.get('Content-Type')):
            for renderer in self.filter_renderers(renderers, content_type):
                if content_type == renderer.format:
                    return renderer, renderer.media_type
        return super().select_renderer(request, renderers, format_suffix)
