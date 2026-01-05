from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import login
from .serializers import SignupSerializer, ProfileSerializer, MyTokenObtainPairSerializer, ChangePasswordSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class SignupAPIView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "User created"}, status=201)




class ProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user.profile)
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileSerializer(
            request.user.profile,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ChangePasswordAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({"message": "Password updated successfully"}, status=200)    