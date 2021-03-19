from django.http import JsonResponse


class UserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"
        response["Access-Control-Allow-Methods"] = "*"
        return response

    def process_exception(self, request, exception):
        if exception.__class__.__name__ in [
            "PermissionError",
            "AuthorizationFailed",
            "AuthenticationFailed",
        ]:
            return JsonResponse({"status": "failed", "msg": f"{exception}"}, status=403)
        else:
            return None