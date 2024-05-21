from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .serializers import (
    UserSerializer,UserViewSerializer,
    
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import viewsets, status







# Create your views here.
class Userlogin(APIView):
    permission_classes = [AllowAny]


    def get_tokens_for_user(self,user):
                    refresh = RefreshToken.for_user(user)
                    return {
                                'refresh': str(refresh),
                                'access': str(refresh.access_token),
                            }
    

    def get(self,request):
        # data = User.objects.all()
        # serializer = UserSerializer(data,many=True) 
        # return Response(serializer.data)
        return Response({"status":"Not Found"},status=status.HTTP_404_NOT_FOUND)

    def post(self,request):
        try:
            query_params = request.data
            print(query_params)
            if "userName" in query_params and "password" in query_params:
                username = query_params["userName"]
                password = query_params["password"]
                user = authenticate(request, username=username, password=password)
                print(user)
                if user is not None:
                    print("inside if condition")
                    login(request, user)
                    token = self.get_tokens_for_user(user)
                    return Response({'status' : True, 'token' : token})
                else:
                    return Response({'status': False})
                
            else:
                return Response({'status': False})
        
        except Exception as e:
             return Response(str(e))


class Userlogout(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            logout(request)
            return Response({'status': True})
        except Exception as e:
             return Response(str(e))

class ViewUser(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    # model = User
    serializer_class = UserViewSerializer
    permission_classes = [IsAuthenticated]
    # queryset = model.objects.all()
    
    
    
    def get(self,request):
        try:
            # meta = request.META
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            print(request.user)
            # user = User.objects.get(pk = request.user.id)
            queryset = User.objects.all()
            serializer = self.get_serializer(queryset,many = True)
            print(token)
            return Response(serializer.data,status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e))
            




class UserCreate(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    # model = User
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    # queryset = model.objects.all()

    
    
    # def get(self,request):
    #     try:
    #         user = User.objects.all()
    #         # all_fields = user._meta.get_fields()
    #         # print(all_fields)
    #         serializers = self.get_serializer(user,many=True)
    #         return Response({"fields":serializers.data})
    #     except Exception as e:
    #          return Response(str(e))


    def post(self,request):
        try:
            data = request.data

            serializers = self.get_serializer(data=data)

            if serializers.is_valid():
                serializers.save()    
                return Response(serializers.data,status=status.HTTP_201_CREATED)
            else:
                return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
             return Response(str(e))
        

