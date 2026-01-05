from django.urls import path
from .views import SignupAPIView, ProfileAPIView, MyTokenObtainPairView, ChangePasswordAPIView

urlpatterns = [
    path('signup/', SignupAPIView.as_view()),
    path('login/', MyTokenObtainPairView.as_view()),
    path('profile/', ProfileAPIView.as_view()),
    path('change-password/', ChangePasswordAPIView.as_view()),
]
