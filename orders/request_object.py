from . import models


def request_object_middleware(get_response):
    def middleware(request):
        models.request_object = request
        response = get_response(request)

        return response

    return middleware
