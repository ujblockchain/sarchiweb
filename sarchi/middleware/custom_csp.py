from django.http import HttpResponseServerError, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden


class CustomCSPMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        print('Content-Security-Policy' in response)
        

        # Check if the response corresponds to a 404 error page
        if isinstance(response, HttpResponseServerError) or isinstance(response, HttpResponseNotFound) or isinstance(
                response, HttpResponseBadRequest) or isinstance(response, HttpResponseForbidden):

            # Apply the relaxed CSP policy for error pages
           response['Content-Security-Policy'] = "default-src 'self'; img-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' https://www.google.com https://www.googletagmanager.com https://www.gstatic.com; font-src 'self' https://fonts.gstatic.com https://use.fontawesome.com https://fonts.gstatic.com;"


        return response
