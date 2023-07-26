from rest_framework import serializers
from . models import CustomUser, DocterModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','name','email','password','username']


class UserLoginSerializer(serializers.ModelSerializer):
     email = serializers.EmailField(max_length=255)
     class Meta:
          model = CustomUser
          fields = ['email','password']


class DocterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocterModel
        fields = ['id','name','place','age','spec','email','blocked']
