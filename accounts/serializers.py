from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer): #serializer for register model

    class Meta:
        model= User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only':True}}   # to hide the password from return response


    def validate(self, attrs):      # validate the inputed attribute
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        return attrs

    def create(self, validated_data, *args):
        user = User.objects.create_user(**validated_data)
        return user
