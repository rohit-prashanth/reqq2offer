from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import (
    EmployeeViewSerializer, PDFGenerationSerializer, ColumnCreationSerializer, ColumnDropDownCreationSerializer
)
from .models import HrTeam, EmployeeDetails, Customer, NewTable, TableDropdownsList
from .create_offer_1 import create_offer
from rec2offer import settings
import re
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.db import connection, models
from django.core.files.storage import FileSystemStorage

# HrTeamView class handles CRUD operations for HR team members.
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

# CreateOfferLetter class handles the creation of offer letters and saves them as PDFs.
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

# ColumnCreationAPIView class handles the creation of new columns in a table.
class ColumnCreationAPIView(GenericAPIView):
    serializer_class = ColumnCreationSerializer

    def get(self, request, format=None):
        table_name = 'ctc_newtable'
        with connection.cursor() as cursor:
            try:
                query = f"""
                    SELECT 
                        c.column_name, 
                        c.data_type,
                        conname AS constraint_name,
                        pg_get_constraintdef(pg_constraint.oid) AS constraint_definition
                    FROM 
                        information_schema.columns c
                    LEFT JOIN 
                        pg_constraint 
                        ON conrelid = (
                            SELECT oid 
                            FROM pg_class 
                            WHERE relname = c.table_name
                        )
                        AND conkey[1] = (
                            SELECT ordinal_position 
                            FROM information_schema.columns 
                            WHERE table_name = c.table_name 
                            AND column_name = c.column_name
                        )
                    WHERE 
                        c.table_name = '{table_name}';
                """
                cursor.execute(query)
                column_details = cursor.fetchall()
                columns = {col[0]: col[1] for col in column_details}
                results = column_details
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(results, status=status.HTTP_200_OK)

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

                if field_type == 'dropdown':
                    options = serializer.validated_data['options']
                    options = tuple(options)
                    query = f"""
                        ALTER TABLE {table_name}
                        ADD COLUMN {column_name} VARCHAR(50),
                        ADD CONSTRAINT chk_{column_name}
                        CHECK ({column_name} IN {options})
                    """

                else:
                    query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {data_type};"

                with connection.cursor() as cursor:
                    cursor.execute(query)

                if field_type == 'dropdown':
                    data = TableDropdownsList(table_name=table_name,column_name=column_name)
                    options = serializer.validated_data['options']
                    data.set_elements(options)
                    data.save()
                    
                    #retrieving list
                    # retrieved = MyModel.objects.get(id=m.id)
                    # elements = retrieved.get_elements()  # returns [1, 2, 3, 4]
                return Response({'message': f'Column {column_name} added to table {table_name}'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# DummyDataAPIView class handles the insertion of dummy data into a table.
class DummyDataAPIView(GenericAPIView):
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

# GetDummyDataAPIView class retrieves data from a table.
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

# DeleteFieldAPIView class handles the deletion of a column from a table.
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

# Example data and schema
example_data = ['name', 'age', 'gender']

example_schema = [
    {
        "column_name": "name",
        "field_type": "text"
    },
    {
        "column_name": "age",
        "field_type": "text"
    },
    {
        "column_name": "email",
        "field_type": "text"
    },
    {
        "column_name": "category",
        "field_type": "dropdown",
        "options": [1, 2]
    },
]
