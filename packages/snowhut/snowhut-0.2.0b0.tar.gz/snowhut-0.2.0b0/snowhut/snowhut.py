import snowflake.connector as sf
import pandas as pd
import json
from snowflake.connector import DictCursor
import os


class Snowflake:
    """Pizza Hut Snowflake connection.
    """
    DEFAULT_PATH = os.path.join(os.path.expanduser('~'), "snowflake_config.json")

    def __init__(self, config_path=DEFAULT_PATH, config='default'):
        with open(config_path) as c:
            cfg = json.load(c)
            self.cfg = cfg[config]

        self.con = sf.connect(
            user=self.cfg["username"],
            password=self.cfg["password"],
            role=self.cfg["role"],
            account=self.cfg["account"],
            warehouse=self.cfg["warehouse"],
            database=self.cfg["database"],
            schema=self.cfg["schema"]
        )

    def execute_query(self, query, from_file=False):
        """Run commands in Snowflake.
        """

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
            results = pd.read_sql(query, self.con)
            return results

        except sf.errors.ProgrammingError as e:
            # default error message
            print(e)
            # customer error message
            print('Error {0} ({1}): {2} ({3})'.format(
                e.errno, e.sqlstate, e.msg, e.sfqid)
                )
        return None
