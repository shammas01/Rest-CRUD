from rest_framework.views import APIView
from . models import User
from . serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime


# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            hashed_password = make_password(password)
            
            user = User.objects.create(
                name = name,
                email = email,
                password = hashed_password
            )

            return Response(UserSerializer(user).data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User Not Found!')
        if not user.check_password(password):
            raise AuthenticationFailed('invalid password!')
        
        payload = {
            'id' : user.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat' : datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'messege':"login successfull",
            'jwt' : token

        }

        return response


class Userview(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            playload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        
        user = User.objects.filter(id=playload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
           

class LogOutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            
            'messege':'logout successfully'
        }

        return response