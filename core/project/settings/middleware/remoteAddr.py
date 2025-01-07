from django.utils.deprecation import MiddlewareMixin


class RemoteAddrMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
            request.META['REMOTE_ADDR'] = ip
