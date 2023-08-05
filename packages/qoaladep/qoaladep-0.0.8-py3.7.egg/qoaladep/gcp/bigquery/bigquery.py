from google.cloud import bigquery

class Bigquery(Object):

    def __init__(self, project_id):
        """[Init function]
        
        Arguments:
            project_id {[string]} -- [Project ID in cloud platform]
        """        
        self.bigquery_client = bigquery.Client(project=project_id)

    def query(self, query_sql):
        """[Get data from table]
        
        Arguments:
            kiquery_sqlnd {[string]} -- [SQL Statement]
        
        Returns:
            result[dict] -- [Dictionary of data]
        """        
        result = []
        try:
            query_job = self.bigquery_client.query(query_sql)
            result = query_job.result()
        except Exception as e:
            print(e)

        return result

    def insert_data(self, database_name, table_name, data):
        list_column_name = list(data.keys())
        list_value_data = list(data.values())

        query_sql = '''insert into {}.{} ({}) values {}'''.format(database_name, table_name, list_column_name, list_value_data)