import json

class DBConnection():

    def __init__(self, pool):
        self.pool = pool 

    def get_session(self):
        return DBSession(self.pool)

class DBSession():

    def __init__(self, pool):
        """
        pool (object): psycopg2 pool instance
        """
        self.pool = pool
        self.connection = pool.getconn()

    def query(self, module_function, *query_params):
        
        query, params, wrapper, many = module_function(*query_params)

        return self._fetch(query, params, wrapper, many)

    def insert(self, module_function, *query_params):

        query, params, wrapper, many = module_function(*query_params)

        return self._upsert(query, params, wrapper, many)

    def update(self, module_function, *query_params):
        
        query, params, wrapper, many = module_function(*query_params)

        return self._upsert(query, params, wrapper, many)

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.pool.putconn(self.connection)


    def _unwrap(self, value, wrapper, many=True):
        if wrapper and not hasattr(wrapper, 'fields'):
            wrapper.fields = DatabaseObject.get_description(self.connection, wrapper)

        if many:
            if wrapper:
                return [wrapper(row) for row in value]
            else:
                return value
        else:
            if wrapper:
                return wrapper(value) if value else None
            else:
                return value

    def _fetch(self, query, params, wrapper=None, many=True):
    
        connection = self.connection

        cursor = connection.cursor()
        cursor.execute(query, params)

        result = cursor.fetchall() if many else cursor.fetchone()

        cursor.close()

        return self._unwrap(result, wrapper, many)

    def _upsert(self, query, params, wrapper=None, many=False):
    
        connection = self.connection

        cursor = connection.cursor()
        cursor.execute(query, params)
        
        result = cursor.fetchall() if many else cursor.fetchone()

        cursor.close()

        return self._unwrap(result, wrapper, many)

class DatabaseObject:

    def __init__(self, row):
        self.row = row

        if not hasattr(self, 'fields'):
            self.fields = DatabaseObject.get_description(self)

        for i, field in enumerate(self.fields):
            setattr(self, field, self.row[i])

    def _get_upsert_value(self, data):

        if data == None:
            return None
        if type(data) == dict:
            return json.dumps(data)
        else:
            return str(data)
    

    @staticmethod
    def get_description(conn, dbObject):

        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {dbObject._TABLE_NAME} LIMIT 0")

        description = [
            descriptor[0] 
            for descriptor in cursor.description
        ]

        return description



    def __repr__(self):
    
        dct = {
            field : getattr(self, field)
            for field in self.fields
        }

        return str(dct)