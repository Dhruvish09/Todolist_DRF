from rest_framework import serializers,validators
from .models import ToDoItem
from django.contrib.auth.models import User


class ToDoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoItem
        fields = ['id', 'title', 'description', 'created_date']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep

    def create(self, validated_data):
        return ToDoItem.objects.create(**validated_data)
    
    def validate_title(self, value):
        # Check if the title already exists
        if ToDoItem.objects.filter(title=value).exists():
            raise serializers.ValidationError('This title is already taken.')
        return value

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.created_date = validated_data.get('created_date', instance.created_date)
        instance.save()
        return instance
    
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email','password')

# Register_Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {
                'required': True,
                'allow_blank': True,
                'validators':[
                    validators.UniqueValidator(User.objects.all(),"A user with that Email already exists.")
                ]             
                }
                }

    def validate_username(self, value):
        # Check if the username already exists
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('This username is already taken.')
        return value

    def validate_email(self, value):
        # Check if the email already exists
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email address is already registered.')
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user

# Login_Serializer
class LoginSerializer(serializers.Serializer):
    model = User

    """
    Serializer for login endpoint.
    """
    class Meta:
        model = User
        fields = ('username', 'password')

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

 