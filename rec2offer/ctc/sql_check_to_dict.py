import re

def sql_check_to_dict(sql_check):
    # Define a regular expression pattern to match the structure of the CHECK constraint
    # pattern = r"CHECK \(\(\((\w+)\)::text = ANY \(\(ARRAY\[(.*)\]::text\[\]\)\)\)\)"

    pattern = r"CHECK \(\(\((\w+)\)::text = ANY \(\(ARRAY\[(.*)\]::character varying\[\]\)::text\[\]\)\)\)"
    
    # Use regex to search for matches in the SQL string
    match = re.search(pattern, sql_check)
    if not match:
        raise ValueError("The provided SQL CHECK constraint does not match the expected format.")
    
    # Extract the column name and the valid values
    column_name = match.group(1)
    values_str = match.group(2)
    
    # Split the values string by commas and remove surrounding single quotes and spaces
    values = [value.strip().strip("'") for value in values_str.split(",")]
    
    # Create the resulting dictionary
    result_dict = {column_name: values}
    
    return result_dict

# Example usage
sql_check = "CHECK (((product_category)::text = ANY ((ARRAY['Electronics'::character varying, 'Clothing'::character varying, 'Books'::character varying, 'Toys'::character varying])::text[])))"
# sql_check = "CHECK (((category)::text = ANY ((ARRAY['Electronics'::character varying, 'Clothing'::character varying, 'Books'::character varying, 'Toys'::character varying])::text[])))"
result = sql_check_to_dict(sql_check)
print(result)
