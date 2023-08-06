import snowflake.connector as sf
import pandas as pd
from snowflake.connector import DictCursor
import os


class Snowflake:
    '''Snowflake Connector class'''


    def __init__(self, credentials=None):
        self.credentials = credentials
        self.con = sf.connect(
            user = self.credentials['USERNAME'],
            password = self.credentials['PASSWORD'],
            role = self.credentials['ROLE'],
            account = self.credentials['ACCOUNT'],
            warehouse = self.credentials['WAREHOUSE'],
            database = self.credentials['DATABASE'],
            schema = self.credentials['SCHEMA'],
            ) if self.credentials is not None else None


    def connect(self, **args):
        ''' Connect to Snowflake Database.
        '''
        if not self.credentials:
            return "Please provide credentials to continue."
        else:
            try:
                self.con = sf.connect(
                    user = self.credentials['USERNAME'],
                    password = self.credentials['PASSWORD'],
                    role = self.credentials['ROLE'],
                    account = self.credentials['ACCOUNT'],
                    warehouse = self.credentials['WAREHOUSE'],
                    database = self.credentials['DATABASE'],
                    schema = self.credentials['SCHEMA'],
                    )
            except:
                print('error connecting.')
        return None


    def disconnect(self):
        self.con.close()
        self.con = None
        return None


    def execute_query(self, query, return_results=True, 
        from_file=False):
        ''' Run commands in Snowflake.
        '''


        def read_query(filepath):
            """Fetch query text.

            Input:
            -------------------------
            file_name:  (str) File name, including suffix. Must be 
                        located in queries folder.

            Output:
            -------------------------
            query_text: (str) Snowflake query string.
            """

            try:
                query_text = open(filepath).read()
                return query_text
            except:
                print("There was an error reading the file.")
                return None


        if from_file:
            try:
                query = read_query(query)
            except:
                print('Error reading query from file.')

        try:
            cursor = self.con.cursor(DictCursor)
            cursor.execute(query)
            if return_results:
                results = cursor.fetchall()
                val = pd.DataFrame(results)
            else:
                val = None
            cursor.close()
            return val

        except sf.errors.ProgrammingError as e:
            # default error message
            print(e)
            # customer error message
            print('Error {0} ({1}): {2} ({3})'.format(
                e.errno, e.sqlstate, e.msg, e.sfqid)
                )
        return None