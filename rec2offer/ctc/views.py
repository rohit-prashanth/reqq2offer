from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from psycopg2.extras import RealDictCursor
from rest_framework import status
from .serializers import (
    EmployeeViewSerializer, PDFGenerationSerializer, ColumnCreationSerializer, ColumnDropDownCreationSerializer,
    EditColumnDropDownCreationSerializer, EditColumnCreationSerializer
)
from .models import HrTeam, EmployeeDetails, Customer, NewTable, TableDropdownsList
from .create_offer_1 import create_offer
from rec2offer import settings
import json
import re
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.db import connection, models
from django.core.files.storage import FileSystemStorage
import psycopg2

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
    
class ColumnCreationAPIView(APIView):
    serializer_class = ColumnCreationSerializer

    def get(self, request, *args, **kwargs):
        try:
            
            # Create a cursor object
            cur = connection.cursor()

            # First query: Fetching all columns from 'ctc_tabledropdownslist'
            cur.execute("SELECT id ,table_name, column_name, column_type, elements FROM public.ctc_tabledropdownslist;")
            colnames1 = [desc[0] for desc in cur.description]
            rows1 = cur.fetchall()

            # Convert rows into a list of dictionaries
            data_from_tabledropdownslist = [dict(zip(colnames1, row)) for row in rows1]

            # Second query: Fetching column names from 'ctc_newtable'
            cur.execute("SELECT column_name,data_type FROM information_schema.columns WHERE table_name = 'ctc_newtable';")
            colnames2 = [desc[0] for desc in cur.description]
            rows2 = cur.fetchall()

            # Convert rows into a list of dictionaries
            data_from_newtable = [dict(zip(colnames2, row)) for row in rows2]
            

            # Close the cursor and connection
            cur.close()
            connection.close()

            # Find common column names in both datasets
            common_columns = set([d1['column_name'] for d1 in data_from_tabledropdownslist]).intersection(
                              set([d2['column_name'] for d2 in data_from_newtable]))

            # Process common columns
            for column_name in common_columns:
                for item in data_from_newtable:
                    if item['column_name'] == column_name:
                        # Find corresponding column info in data_from_tabledropdownslist
                        for dropdown_item in data_from_tabledropdownslist:
                            if dropdown_item['column_name'] == column_name:
                                item['data_type'] = dropdown_item['column_type']
                                item['elements'] = json.loads(dropdown_item['elements'])
                        break  # Exit loop after updating

            # Prepare combined data for JSON response
            combined_data = {
                'data_from_newtable': data_from_newtable
            }

            # Convert the data to JSON format
            json_data = json.dumps(data_from_newtable)

            # Return the JSON response
            return Response(json.loads(json_data))

        except psycopg2.Error as e:
            # Handle PostgreSQL errors
            return Response({'error': str(e)}, status=500)

        except Exception as e:
            # Handle other exceptions
            return Response({'error': str(e)}, status=500)

    def post(self, request):
        try:
            field_type_list = ['dropdown','radio','checkbox']
            if request.data.get('field_type') in field_type_list:
                print(request.data.get('field_type'))
                serializer = ColumnDropDownCreationSerializer(data=request.data)
            else:
                serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                print("inside is_valid")
                column_name = serializer.validated_data['column_name']
                data_type = serializer.validated_data['data_type']
                field_type = serializer.validated_data['field_type']
                table_name = 'ctc_newtable'
                if field_type == 'dropdown' or field_type == 'radio':
                    options = serializer.validated_data['options']
                    options = tuple(options)
                    query = f"""
                        ALTER TABLE {table_name}
                        ADD COLUMN {column_name} VARCHAR(50),
                        ADD CONSTRAINT chk_{column_name}
                        CHECK ({column_name} IN {options})
                    """
                elif field_type == 'checkbox':
                    query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} BOOLEAN;"
                else:
                    if new_data_type == 'text':
                        new_data_type = "varchar"
                    query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {data_type};"

                with connection.cursor() as cursor:
                    cursor.execute(query)

                if field_type == 'dropdown' or field_type == 'radio':
                    data = TableDropdownsList(table_name=table_name,column_name=column_name,column_type=field_type)
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
        
    
    def put(self,request, column_name = None):
        try:
            field_type_list = ['dropdown','radio','checkbox']
            print("inside field type list")
            if request.data.get('new_field_type') in field_type_list:
                print("inside field type list")
                print(request.data.get('field_type'))
                serializer = EditColumnDropDownCreationSerializer(data=request.data)
            else:
                serializer = EditColumnCreationSerializer(data=request.data)
            if serializer.is_valid():
                print("inside is_valid")
                old_column_name = serializer.validated_data['old_column_name']
                old_data_type = serializer.validated_data['old_data_type']
                old_field_type = serializer.validated_data['old_field_type']
                new_column_name = serializer.validated_data['new_column_name']
                new_data_type = serializer.validated_data['new_data_type']
                new_field_type = serializer.validated_data['new_field_type']
                table_name = 'ctc_newtable'
                if new_data_type == 'text':
                    new_data_type = "varchar"
                if new_field_type == 'dropdown' or new_field_type == 'radio':
                    options = serializer.validated_data['options']
                    options = tuple(options)
                    # query = f"""
                    #     ALTER TABLE {table_name}
                    #     ADD COLUMN {column_name} VARCHAR(50),
                    #     ADD CONSTRAINT chk_{column_name}
                    #     CHECK ({column_name} IN {options})
                    # """
                    
                    # query = f"""BEGIN;
                    #         ALTER TABLE {table_name} RENAME COLUMN {old_column_name} TO {new_column_name};
                    #         ALTER TABLE {table_name} ALTER COLUMN {new_column_name} TYPE {new_data_type} USING {new_column_name}::VARCHAR(50);
                    #         ALTER TABLE {table_name} ADD CONSTRAINT chk_{new_column_name} CHECK ({new_column_name} IN {options});
                    #         COMMIT;"""

                    query = f"""
                                BEGIN;

                                -- Step 1: Rename the column
                                ALTER TABLE {table_name}
                                RENAME COLUMN {old_column_name} TO {new_column_name};

                                -- Step 2: Alter the column type to VARCHAR(50)
                                ALTER TABLE {table_name}
                                ALTER COLUMN {new_column_name} TYPE VARCHAR(50)
                                USING {new_column_name}::VARCHAR(50);

                                -- Step 3: Add a check constraint
                                ALTER TABLE {table_name}
                                ADD CONSTRAINT chk_{new_column_name} CHECK ({new_column_name} IN {options});

                                COMMIT;
                    """
                elif new_field_type == 'checkbox':
                    # query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} BOOLEAN;"
                    query = f""" 
                            BEGIN;
                            ALTER TABLE {table_name} RENAME COLUMN {old_column_name} TO {new_column_name};
                            ALTER TABLE {table_name} ALTER COLUMN {new_column_name} TYPE {new_data_type} USING {new_column_name}::BOOLEAN;
                            COMMIT;

                            """
                else:
                    
                    # query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {data_type};"
                    print("inside else part")
                    listdatatypes = ['radio','dropdown']
                    if old_column_name == new_column_name and old_data_type in listdatatypes and new_data_type not in listdatatypes:
                        print("changing listdatarypes")
                      
                        query = f""" 
                            BEGIN;
                            ALTER TABLE {table_name} DROP CONSTRAINT chk_{new_column_name};
                            ALTER TABLE {table_name} ALTER COLUMN {new_column_name} TYPE {new_data_type} USING {new_column_name}::{new_data_type};
                            COMMIT;

                            """
                    else:
                        
                        query = f""" 
                                BEGIN;
                                ALTER TABLE {table_name} RENAME COLUMN {old_column_name} TO {new_column_name};
                                ALTER TABLE {table_name} ALTER COLUMN {new_column_name} TYPE {new_data_type} USING {new_column_name}::{new_data_type};
                                COMMIT;

                                """

                with connection.cursor() as cursor:
                    cursor.execute(query)

                if new_field_type == 'dropdown' or new_field_type == 'radio':
                    data = TableDropdownsList(table_name=table_name,column_name=new_column_name,column_type=new_field_type)
                    options = serializer.validated_data['options']
                    data.set_elements(options)
                    data.save()
                
                elif new_field_type == 'text' or new_field_type == 'boolean':
                    obj = TableDropdownsList.objects.filter(table_name=table_name,column_name=column_name)
                    if obj:
                        print("inside row delete")
                        obj.delete()
                    #retrieving list
                    # retrieved = MyModel.objects.get(id=m.id)
                    # elements = retrieved.get_elements()  # returns [1, 2, 3, 4]
                return Response({'message': f'Column {new_column_name} updated to table {table_name}'}, status=status.HTTP_200_OK)
            
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
                # sql_script = f"""
                #     ALTER TABLE {table_name} DROP COLUMN {field_name};
                # """
                sql_script = f"""
                                BEGIN;

                                -- Step 1: Drop the column
                                ALTER TABLE {table_name}
                                DROP COLUMN {field_name};

                                -- Step 2: Drop any check constraints related to the dropped column
                                ALTER TABLE {table_name}
                                DROP CONSTRAINT IF EXISTS chk_{field_name};


                                COMMIT;

                                """
                cursor.execute(sql_script)
            return Response({'message': f'Field {field_name} deleted successfully from table {table_name}'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


