from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView,  TokenViewBase, TokenObtainSlidingView,TokenRefreshSlidingView
from rest_framework_simplejwt.serializers import  TokenObtainSerializer
from myapi.core import views
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken, UntypedToken
from django.utils.six import text_type


class TokenObtainPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super(TokenObtainPairSerializer, self).validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = text_type(refresh)
        data['access'] = text_type(refresh.access_token)

        return data

class GetToken(TokenViewBase):
    serializer_class = TokenObtainPairSerializer







urlpatterns = [
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('api/token/', GetToken.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
