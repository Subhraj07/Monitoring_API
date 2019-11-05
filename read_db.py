import psycopg2
import psycopg2.extras
import pandas as pd
from config.Config import Config


def read_sql(query):
    try:
        connection = psycopg2.connect(user=Config.user,
                                      password=Config.password,
                                      host=Config.host,
                                      port=Config.port,
                                      database=Config.database)

        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)  # This line allows dictionary access.
        # select some records into "rows"

        cursor.execute(query)
        mobile_records = cursor.fetchall()

        column_names = []
        for i in cursor.description:
            column_names.append(i[0])

        df = pd.DataFrame(mobile_records, columns=column_names)

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return df


def read_data():
    sql = "select * from {0}".format("public.edl_table")
    return read_sql(sql)


def read_data_days(days):
    sql = "select * from {0} limit {1}".format("public.edl_table", days)
    return read_sql(sql)
