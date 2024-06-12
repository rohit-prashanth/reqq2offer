from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth import authenticate

from .serializers import (EmployeeViewSerializer, EmployeeDetailsSerializer, 
                        CustomerSerializer,PDFGenerationSerializer,ColumnCreationSerializer)
from .models import HrTeam, EmployeeDetails, Customer
from .create_offer_1 import create_offer
from rec2offer.settings import BASE_DIR
import os
from rec2offer import settings
from django.db import connection

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.db import connection, models
from django.core.management import call_command
from django.apps import apps

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

    # def post(self, request):
    #     """
    #     Handle POST requests to create a new HR team member.
    #     """
    #     try:
    #         data = request.data
            
    #         if 'ctc' in data and 'name' in data and 'designation' in data:
    #             offer = create_offer(data)
    #             print(offer)
    #             if offer:
    #                 return Response(offer, status=status.HTTP_201_CREATED)
    #             else:
    #                 return Response({"error":"Salary structure has not created."}, status=status.HTTP_400_BAD_REQUEST)
    #         else:
    #             return Response({"error":"Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

    #     except Exception as e:
    #         return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
    
    def post(self, request, format=None):
        serializer = PDFGenerationSerializer(data=request.data)
        if serializer.is_valid():
            # Get data from serializer
            name = serializer.validated_data['name']
            designation = serializer.validated_data['designation']
            # Generate PDF
            # pdf_filename = self.generate_pdf(name, designation)
            pdf_filename = create_offer(request.data)

            # Save PDF to media directory
            if pdf_filename:
                # print(pdf_filename.getvalue(), type(pdf_filename))
                filename = f"offer_letters/{name}_{designation}.pdf"
                media_path = os.path.join(settings.MEDIA_ROOT, filename)
                with open(media_path, 'wb') as f:
                    f.write(pdf_filename.getvalue())
                # Return response
                return Response({"status":"created successfully","path": os.path.join(settings.MEDIA_URL, filename)}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error":"Salary structure has not created."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def generate_pdf(self, name, designation):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{name}_{designation}.pdf"'
        # Create PDF content
        p = canvas.Canvas(response, pagesize=letter)
        p.drawString(100, 750, "Name: {}".format(name))
        p.drawString(100, 730, "Designation: {}".format(designation))
        # Add more content as needed
        p.showPage()
        p.save()
        return response
    

class ColumnCreationAPIView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeViewSerializer
    queryset = HrTeam.objects.all()
    
    # def post(self, request):
    #     try:
    #         serializer = ColumnCreationSerializer(data=request.data)
    #         if serializer.is_valid():
    #             column_name = serializer.validated_data['column_name']
    #             data_type = serializer.validated_data['data_type']
    #             table_name = serializer.validated_data['table_name']

    #             with connection.cursor() as cursor:
    #                 # Execute raw SQL to alter table and add column
    #                 query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {data_type};"
    #                 cursor.execute(query)
                
    #             return Response({'message': f'Column {column_name} added to table {table_name}'}, status=status.HTTP_200_OK)
    #         else:
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        try:
            serializer = ColumnCreationSerializer(data=request.data)
            if serializer.is_valid():
                column_name = serializer.validated_data['column_name']
                data_type = serializer.validated_data['data_type']
                table_name = serializer.validated_data['table_name']
            # table_name = request.data.get('table_name')
            # column_name = request.data.get('column_name')
            # column_type = request.data.get('column_type')

                if not table_name or not column_name or not data_type:
                    return Response({'error': 'Missing parameters'}, status=status.HTTP_400_BAD_REQUEST)

                # Validate column type
                column_types = {
                    'char': 'CharField(max_length=255)',
                    'text': 'TextField()',
                    'integer': 'IntegerField()',
                    'boolean': 'BooleanField()'
                }

                if data_type not in column_types:
                    return Response({'error': 'Invalid column type'}, status=status.HTTP_400_BAD_REQUEST)

                myapp = 'ctc'
                
                # Dynamically add the new field to the model
                model = apps.get_model(myapp, table_name)
                field = models.CharField(max_length=255,null=True) if data_type == 'char' else models.TextField(null=True) if data_type == 'text' else models.IntegerField(null=True) if data_type == 'integer' else models.BooleanField(default=False)

                field.contribute_to_class(model, column_name)

                # Create a migration for the new field
                call_command('makemigrations', myapp)
                call_command('migrate', myapp)

                return Response({'status': 'column added'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
