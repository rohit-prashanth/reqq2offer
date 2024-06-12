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
from .models import models
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import viewsets, status

from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.core.files.storage import FileSystemStorage
import base64
from django.core.files.base import ContentFile
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
import os


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
        
class GetId(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserViewSerializer
    queryset = User.objects.all()  # Set the queryset to retrieve all User objects

    def get(self, request, id=None):  # Add id parameter to the method
        try:
            if id is None:
                return Response({"error": "ID parameter is missing."}, status=status.HTTP_400_BAD_REQUEST)
            print(id)
            user = User.objects.get(pk=id)  # Use the queryset properly and filter by id
            serializers = self.get_serializer(user)
            return Response({"fields": serializers.data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data
            serializers = self.get_serializer(data=data)

            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UploadImageView(APIView):
    parser_classes = [JSONParser]

    # def post(self, request, *args, **kwargs):
    #     image = request.data.get('image')
    #     if not image:
    #         return JsonResponse({'error': 'No image provided'}, status=400)
    #     fs = FileSystemStorage()
    #     # print(image)
    #     # Process the image data here (e.g., save to file, perform analysis, etc.)
    #     # For this example, let's just acknowledge receipt

    #     # save the image on MEDIA_ROOT folder
    #     file_name = fs.save("photo",image)

    #     # get file url with respect to `MEDIA_URL`
    #     # file_url = fs.url(file_name)
    #     # return HttpResponse(file_url)
        
    #     if pdf_filename:
    #             # print(pdf_filename.getvalue(), type(pdf_filename))
    #             filename = f"offer_letters/{name}_{designation}.pdf"
    #             media_path = os.path.join(settings.MEDIA_ROOT, filename)
    #             with open(media_path, 'wb') as f:
    #                 f.write(pdf_filename.getvalue())
    #             # Return response
    #             return Response({"status":"created successfully","path": os.path.join(settings.MEDIA_URL, filename)}, status=status.HTTP_201_CREATED)
    #         else:
    #             return Response({"error":"Salary structure has not created."}, status=status.HTTP_400_BAD_REQUEST)

    #     return JsonResponse({'status': 'Image received successfully'})


    def post(self, request, *args, **kwargs):
        image_data = request.data.get('image')
        if not image_data:
            return JsonResponse({'error': 'No image provided'}, status=400)

        # Decode the base64 image data
        format, imgstr = image_data.split(';base64,') 
        ext = format.split('/')[-1]  # Extract the file extension
        data = ContentFile(base64.b64decode(imgstr), name=f'upload.{ext}')
        
        # Define the directory and file path
        file_path = os.path.join('media\\Images', f'captured_image2.{ext}')

        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Save the image file
        with open(file_path, 'wb') as f:
            f.write(data.read())
        
        return JsonResponse({'status': 'Image received and saved successfully', 'file_path': file_path})