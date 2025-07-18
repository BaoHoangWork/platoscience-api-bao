from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth.models import AnonymousUser
from apps.users.models import User
class CookieJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        token = request.COOKIES.get('access_token')
        if token is None:
            return None
        
        try:
            validated_token = self.get_validated_token(token)
            
            user_id = validated_token.payload.get('id')

            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    if user.is_verified:
                        return (user, validated_token)
                    else:
                        return None
                    return (user, validated_token)
                except User.DoesNotExist:
                    return None
            return None
                
        except TokenError:
            return None
