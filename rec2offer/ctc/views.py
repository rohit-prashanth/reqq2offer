from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import (
    EmployeeViewSerializer, PDFGenerationSerializer, ColumnCreationSerializer,ColumnDropDownCreationSerializer
)
from .models import HrTeam, EmployeeDetails, Customer, NewTable
from .create_offer_1 import create_offer
from rec2offer import settings


# Imaginary function to handle an uploaded file.


import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.db import connection, models
from django.core.files.storage import FileSystemStorage


class HrTeamView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeViewSerializer
    queryset = HrTeam.objects.all()

    def get(self, request, id=None):
        try:
            if id is None:
                hr_team_members = self.get_queryset()
                serializer = self.get_serializer(hr_team_members, many=True)
            else:
                hr_member = get_object_or_404(self.queryset, pk=id)
                serializer = self.get_serializer(hr_member)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("Created successfully", status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)


class CreateOfferLetter(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PDFGenerationSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            designation = serializer.validated_data['designation']
            
            # Generate PDF
            pdf_filename = create_offer(request.data)
            
            # Save PDF to media directory
            if pdf_filename:
                filename = f"offer_letters/{name}_{designation}.pdf"
                media_path = os.path.join(settings.MEDIA_ROOT, filename)
                with open(media_path, 'wb') as f:
                    f.write(pdf_filename.getvalue())
                return Response({"status": "Created successfully", "path": os.path.join(settings.MEDIA_URL, filename)}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Salary structure has not been created."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ColumnCreationAPIView(GenericAPIView):
    serializer_class = ColumnCreationSerializer

    def post(self, request):
        try:
            if request.data['field_type'] == 'dropdown':
                serializer = ColumnDropDownCreationSerializer(data=request.data)
            else:
                serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                column_name = serializer.validated_data['column_name']
                data_type = serializer.validated_data['data_type']
                field_type = serializer.validated_data['field_type']
                table_name = 'ctc_newtable'
                print(field_type)
                if field_type == 'dropdown':
                    options = serializer.validated_data['options']
                    options = tuple(options)
                    query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} ENUM{options};"
                else:
                    query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {data_type};"
                    
                with connection.cursor() as cursor:
                    cursor.execute(query)
                
                return Response({'message': f'Column {column_name} added to table {table_name}'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DummyDataAPIView(GenericAPIView):

    def get(self, request, format=None):
        table_name = 'ctc_newtable'
        
        with connection.cursor() as cursor:
            try:
                cursor.execute(f'SELECT * FROM {table_name}')
                columns = [col[0] for col in cursor.description if col[0] != 'id']  # Exclude 'id' column
                results = columns
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(results, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        table_name = 'ctc_newtable'
        data = request.data

        if not isinstance(data, dict):
            return Response({'error': 'Data must be a dictionary'}, status=status.HTTP_400_BAD_REQUEST)

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        values = list(data.values())

        try:
            with connection.cursor() as cursor:
                query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
                cursor.execute(query, values)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'Record saved'}, status=status.HTTP_201_CREATED)


class GetDummyDataAPIView(APIView):

    def get(self, request, format=None):
        table_name = 'ctc_newtable'
        
        with connection.cursor() as cursor:
            try:
                cursor.execute(f'SELECT * FROM {table_name}')
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
                results = [dict(zip(columns, row)) for row in rows]

                cursor.execute(f"""
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = '{table_name}'
                """)
                column_details = cursor.fetchall()
                column_info = {col[0]: col[1] for col in column_details}
                
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        response_data = {
            'columns': column_info,
            'rows': results
        }
        return Response(response_data)
    
class DeleteFieldAPIView(APIView):

    def delete(self, request, field_name, format=None):
        table_name = 'ctc_newtable'

        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    ALTER TABLE {table_name} DROP COLUMN {field_name};
                """)
            
            return Response({'message': f'Field {field_name} deleted successfully from table {table_name}'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
# class FileDataAPIView(APIView):
   

    # def post(self, request, format=None):
    #     table_name = 'ctc_newtable'

    #     try:
    #         uploaded_file = request.FILES['upload']
    #         fs = FileSystemStorage(location=settings.MEDIA_ROOT)
    #         filename = fs.save(uploaded_file.name, uploaded_file)
    #         uploaded_file_url = fs.url(filename)
            
    #         with connection.cursor() as cursor:
    #             cursor.execute(f"""
    #                 INSERT INTO {table_name} (file_url) VALUES (%s)
    #             """, [uploaded_file_url])
            
    #         return Response({'message': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)

    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    