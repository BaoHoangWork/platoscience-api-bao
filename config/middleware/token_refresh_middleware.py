from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.http import JsonResponse

class TokenRefreshMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')
        if access_token:
            try:
                AccessToken(access_token)
            except TokenError:
                if refresh_token:
                    try:
                        new_access_token = RefreshToken(refresh_token).access_token
                        response = self.get_response(request)
                        response.set_cookie('access_token', str(new_access_token), httponly=True, samesite='Lax')
                        return response
                    except TokenError:
                        return JsonResponse({'error': 'Refresh token expired, please log in again'}, status=401)
                else:
                    return JsonResponse({'error': 'Authentication required'}, status=401)

        return self.get_response(request)
