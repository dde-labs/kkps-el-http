import os

from dotenv import load_dotenv
import mysql.connector
from mysql.connector.errors import DatabaseError

load_dotenv()


try:
    cnx = mysql.connector.connect(
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        host='127.0.0.1',
        database='db'
    )
    cnx.close()
except DatabaseError:
    raise ValueError(
        'Database does not valid with configuration or it does not provisioning'
    ) from None
