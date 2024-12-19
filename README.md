import mysql.connector

def execute_sql_query(query):
    try:
        # Define your database connection parameters
        config = {
            'user': 'root',
            'password': 'root',
            'host': '127.0.0.1',  # Replace '127.0.0.1' with the correct host
            'database': 'commandcenterdb_dev'
        }

        # Connect to the database
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            print("Database connected")

        cursor = conn.cursor()

        # Execute the query
        cursor.execute(query)

        # Fetch the results
        results = cursor.fetchall()

        # Get the column names
        column_names = [i[0] for i in cursor.description]

        # Close the connection
        cursor.close()
        conn.close()

        return column_names, results

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return [], []

# Example usage
if __name__ == "__main__":
    query = "SELECT * FROM pdrmrawmaterial;"
    columns, data = execute_sql_query(query)
    print("Columns:", columns)
    print("Data:", data)
