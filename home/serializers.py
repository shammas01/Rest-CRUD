from rest_framework import serializers
from . models import User, DocterModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','email','password','username']



class DocterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocterModel
        fields = ['id','name','place','age','spec','email','blocked']
