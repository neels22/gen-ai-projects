from langchain_community.utilities import SQLDatabase

def initialize_database():
    """
    Initialize the SQLDatabase object and return it along with schema.
    """
    try:
        db_user = "root"
        db_password = "root"
        db_host = "localhost"
        db_name = "sample"
        port = '3306'
        db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{port}/{db_name}")
        schema = db.get_table_info()
        return db, schema
    except Exception as e:
        print(f"Error initializing database: {e}")
        return None, None



# Now you can use the 'db' and 'schema' variables as needed
