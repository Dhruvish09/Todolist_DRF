from django.urls import path
from restapp import views
from .views import UserLoginView, UserRegistrationView

urlpatterns = [
    path('todoapi/',views.TodoAPI.as_view()),
    path('todoapi/<int:pk>/',views.TodoAPI.as_view()),
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/login/', UserLoginView.as_view(), name='login')
]
