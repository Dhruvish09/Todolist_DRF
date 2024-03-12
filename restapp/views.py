from .models import ToDoItem
from .seriealizers import UserSerializer, RegisterSerializer,LoginSerializer,ToDoItemSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from restapp.renderers import UserRenderer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404

# Todo Crud API
@method_decorator(csrf_exempt, name='dispatch')
class TodoAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ToDoItem.objects.all()
    serializer_class = ToDoItemSerializer


    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='Bearer <your_access_token>', required=True),
        ],
        responses={
            200: ToDoItemSerializer,
            201: 'Data Created',
            400: 'Bad Request',
            401: 'Unauthorized',
            404: 'Not Found',
        },
    )
    def get(self, request, pk=None , *args, **kwargs):
        id =  pk
        try:
            if id is not None:
                todo = ToDoItem.objects.get(id=id)
                serializer = ToDoItemSerializer(todo)
                return Response(serializer.data)
            else:
                todo = ToDoItem.objects.all()
                serializer = ToDoItemSerializer(todo, many=True)
                return Response(serializer.data)
        except Exception as e:
            print(str(e))
            return Response({'msg':'Given id {} is invalid!!!'.format(id)}, status=status.HTTP_404_NOT_FOUND)
        finally:
            print("Thanx for your response\U0001F64F")


    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='Bearer <your_access_token>', required=True),
    ],
    request_body=ToDoItemSerializer,
    responses={
        201: 'Data Created',
        400: 'Bad Request',
        401: 'Unauthorized',
        405: 'Method Not Allowed',
    },
    )
    def post(self, request, *args, **kwargs):
        # If the URL pattern contains a valid pk (ID), return Method Not Allowed
        if 'pk' in kwargs:
            return Response({'msg': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        # Otherwise, continue with the normal POST logic for creating new items
        json_data = request.data
        serializer = ToDoItemSerializer(data=json_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='Bearer <your_access_token>', required=True),
        openapi.Parameter('pk', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='ID of the ToDoItem'),
    ],
    request_body=ToDoItemSerializer,
    responses={
        200: ToDoItemSerializer,
        201: 'Data Updated',
        400: 'Bad Request',
        401: 'Unauthorized',
        404: 'Not Found',
    },
    )
    def put(self, request, pk=None, *args, **kwargs):
        # Ensure pk is converted to an integer
        id = int(pk) if pk is not None else None

        # Print or log the id value to troubleshoot
        print(f"ID from request: {id}")

        # Use get_object_or_404 for cleaner code
        todo = get_object_or_404(ToDoItem, id=id)

        serializer = ToDoItemSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Data Updated!!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg': 'Something is Wrong!!!'}, status=status.HTTP_400_BAD_REQUEST)



    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='Bearer <your_access_token>', required=True),
        ],
        responses={
            201: 'Data Deleted',
            401: 'Unauthorized',
            404: 'Not Found',
        },
    )
    def delete(self, request, pk=None, format=None):
        id =  pk
        todos = ToDoItem.objects.filter().values_list('id', flat=True)
        ids = list(todos)

        if id in ids:
            todo = ToDoItem.objects.get(id=id)
            todo.delete()
            return Response({'msg':'Data Deleted!!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':'Given id {} is invalid!!!'.format(id)}, status=status.HTTP_404_NOT_FOUND) 

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
    }

class UserRegistrationView(generics.GenericAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = UserSerializer
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(generics.GenericAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = LoginSerializer
    
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
          token = get_tokens_for_user(user)
          return Response({'token':token,'username': user.username,'user_id': user.pk, 'msg':'Login Success'}, status=status.HTTP_200_OK)
        else:
          return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

