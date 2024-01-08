import mysql.connector


class Connection:
    def __init__(self, db_config):
        print(f"This is db: {db_config['database']}")
        self.connection = mysql.connector.connect(**db_config)
        self.cursor = self.connection.cursor()

    def insert(self, model_instance):
        print(model_instance)
        # Assuming model_instance is a dictionary with keys corresponding to column names
        # Adjust the column names based on your actual database schema
        columns = ', '.join(model_instance.keys())
        values = ', '.join(['%s' for _ in model_instance.values()])
        query = f'INSERT INTO your_table ({columns}) VALUES ({values})'
        self.cursor.execute(query, tuple(model_instance.values()))
        self.connection.commit()
        # MySQL does not have an equivalent refresh method, so returning None
        return None

    def fetch(self, sql_st):
        self.cursor.execute(sql_st)
        return self.cursor.fetchall()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        if not exc_type:
            pass
        self.connection.close()

if __name__== '__main__':
    # Example usage:
    db_config = {
        'host': 'your_mysql_host',
        'user': 'your_mysql_user',
        'password': 'your_mysql_password',
        'database': 'your_mysql_database',
    }
    with Connection(db_config) as conn:
        data = {'column1': 'value1', 'column2': 'value2'}
        conn.insert(data)
        result = conn.fetch('SELECT * FROM your_table')
        print(result)
