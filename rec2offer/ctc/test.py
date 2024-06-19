from django.http import JsonResponse
from django.db import connection

def fetch_data_view(request):
    try:
        # Replace 'ctc_newtable' with your actual table name
        table_name = 'ctc_newtable'

        # Write your raw SQL query
        query = f"SELECT id, name, dsfsd, newfield, catogieries, fruits FROM {table_name};"

        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]  # Fetch column names from cursor
            rows = cursor.fetchall()

            # Convert rows to a list of dictionaries
            data = [
                dict(zip(columns, row))
                for row in rows
            ]

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
