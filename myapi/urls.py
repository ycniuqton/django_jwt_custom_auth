from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView,  TokenViewBase, TokenObtainSlidingView,TokenRefreshSlidingView
from rest_framework_simplejwt.serializers import  TokenObtainSerializer
from myapi.core import views
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken, UntypedToken, AccessToken
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




def q_authen(func):
    def inner1(*args, **kwargs):
        print("first",args)
        try:
            auth_header = args[1].META["HTTP_AUTHORIZATION"][7:]
            AccessToken(auth_header)
        except:
            return Response({"success":False})
            pass
        result = func(*args, **kwargs)
        return result


    return inner1



from rest_framework.response import Response
from rest_framework.views import APIView
class MyLogin(APIView):
    def post(self, request):
        rf  = RefreshToken()
        rf["user_id"] = 1

        content = {'access_token': text_type(rf.access_token),'refresh_token':text_type(rf)}
        return Response(content)

class RefreshTK(APIView):
    serializer_class = TokenObtainPairSerializer
    def post(self,request):
        refresh = RefreshToken(request.data['refresh'])
        data = {'access': text_type(refresh.access_token)}
        return Response(data)


class HelloView(APIView):
    @q_authen
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)



urlpatterns = [
    path('hello/', HelloView.as_view(), name='hello'),
    path('api/token/', GetToken.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/refresh2/', RefreshTK.as_view(), name='token_refresh'),
    path('login/',MyLogin.as_view())
]
