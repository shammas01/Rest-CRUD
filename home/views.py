from rest_framework.views import APIView
from . models import User, DocterModel
from . serializers import UserSerializer,DocterSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            name = serializer.validated_data.get('name')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            hashed_password = make_password(password)
            
            user = User.objects.create(
                username = username,
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



class UserDeleteView(APIView):
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Response('User doesent exist')
        

    def delete(self, request, username):
        user = self.get_object(username)
        user.delete()
        return Response('user was deleted')




class DocterRegisterview(APIView):
    def post(self, request):
        serializer = DocterSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            place =  serializer.validated_data.get('place')
            age = serializer.validated_data.get('age')
            spec = serializer.validated_data.get('spec')
            email = serializer.validated_data.get('email')


            docter = DocterModel.objects.create(
                name = name,
                place = place,
                age = age,
                spec = spec,
                email = email
            )

            return Response(DocterSerializer(docter).data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def get(self,request):
        docter = DocterModel.objects.all()
        serializer = DocterSerializer(docter,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class DocterDetail(APIView):
    def get(self, request, id):
        try:
            docter = DocterModel.objects.get(id=id)
            serializer = DocterSerializer(docter)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DocterModel.DoesNotExist:
            return Response({'message': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)
    


class DocterEdit(APIView):
    def put(self, request, id):
        try:
            docter = DocterModel.objects.get(id=id)
        except DocterModel.DoesNotExist:
            return Response({"detail": "Doctor with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DocterSerializer(docter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class Doctorblock(APIView):
    def patch(self, request, id):
        try:
            docter = DocterModel.objects.get(id=id)
        except DocterModel.DoesNotExist:
            return Response({"detail": "Doctor with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        action = request.query_params.get('action', None)
        if action not in ['block', 'unblock']:
            return Response({"detail": "Invalid action. Use 'block' or 'unblock' as the query parameter."}, status=status.HTTP_400_BAD_REQUEST)

        if action == 'block':
            docter.blocked = True
        elif action == 'unblock':
            docter.blocked = False

        docter.save()

        return Response(DocterSerializer(docter).data, status=status.HTTP_200_OK)



class DocterDelete(APIView):
    def delete(self, request, id):
        docter = DocterModel.objects.get(id=id) 
        docter.delete()
        return Response("Docter was deleted",status=status.HTTP_200_OK)