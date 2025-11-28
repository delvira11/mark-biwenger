import psycopg
#https://sqlbolt.com/

DB_NAME = "mark_database"


try:
    # You cannot create a new database while connected to that database (since it doesn’t exist yet). So we connect to the default admin database called postgres.
    conn = psycopg.connect(
        dbname = "postgres", # Se queda como postgres porque nos tenemos que conectar a una base de datos existente para ejecutar "CREATE DATABASE" y el admin por defecto siempre es "postgres"
        user = "postgres",
        password = "Yoquesetio1",
        host = "localhost",
        port = 5432
    )

    conn.autocommit = True
    cursor = conn.cursor() # The cursor is what sends SQL commands to PostgreSQL

    cursor.execute(f"CREATE DATABASE {DB_NAME}") # SQL code

    print(f"Database '{DB_NAME}' created successfully.")


except Exception as e:
    print("Error: ", e)

# Close connection regardless of success
finally:
    if conn:
        cursor.close()
        conn.close()