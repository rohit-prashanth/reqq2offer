from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from .serializers import EmployeeViewSerializer, EmployeeDetailsSerializer, CustomerSerializer
from .models import HrTeam, EmployeeDetails, Customer
from .create_offer_1 import create_offer
from rec2offer.settings import BASE_DIR

# Create your views here.
class HrTeamView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeViewSerializer
    queryset = HrTeam.objects.all()

    def get(self, request, id=None):
        """
        Handle GET requests for HrTeam.
        If id is provided, fetch a specific HR team member.
        If id is not provided, fetch all HR team members.
        """
        try:
            if id is None:
                # Fetch all HR team members
                hr_team_members = self.get_queryset()
                serializer = self.get_serializer(hr_team_members, many=True)
                return Response({"fields": serializer.data}, status=status.HTTP_200_OK)
            else:
                # Fetch a specific HR team member by ID
                # hr_member = get_object_or_404(self.queryset, pk=id)
                hr_member = HrTeam.objects.get(pk=id)
                serializer = self.get_serializer(hr_member)
                return Response({"fields": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """
        Handle POST requests to create a new HR team member.
        """
        try:
            data = request.data
            serializer = self.get_serializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response("created successfully", status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        

class CreateOfferLetter(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeViewSerializer
    queryset = HrTeam.objects.all()

    def post(self, request):
        """
        Handle POST requests to create a new HR team member.
        """
        try:
            data = request.data
            
            if 'ctc' in data and 'name' in data and 'designation' in data:
                offer = create_offer(data)
                print(offer)
                if offer:
                    return Response({"status":"created successfully"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error":"Salary structure has not created."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":"Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
