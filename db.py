import os

from dotenv import load_dotenv
import mysql.connector
from mysql.connector.errors import DatabaseError

from models import HistDevidend, DelistedComp


load_dotenv()


def able_to_connect() -> bool:
    try:
        cnx = mysql.connector.connect(
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            host='127.0.0.1',
            database='db'
        )
        cnx.close()
        return True
    except DatabaseError:
        return False


def insert_row_hist_devidends(data: HistDevidend):
    cnx = mysql.connector.connect(
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        host='127.0.0.1',
        database='db'
    )
    cursor = cnx.cursor()
    add_hist_devidends = (
        "INSERT INTO hist_devidends ("
        "symbol, date, label, adjDividend, dividend, recordDate, paymentDate, "
        "declarationDate ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    )
    cursor.execute(
        add_hist_devidends,
        (
            data.symbol,
            data.date,
            data.label,
            data.adjDividend,
            data.dividend,
            data.recordDate,
            data.paymentDate,
        ),
    )
    print(cursor.lastrowid)
    cnx.commit()
    cursor.close()
    cnx.close()


def insert_row_delisted_comp(data: DelistedComp):
    cnx = mysql.connector.connect(
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        host='127.0.0.1',
        database='db'
    )
    cursor = cnx.cursor()
    add_hist_devidends = (
        "INSERT INTO delisted_comp ("
        "symbol, companyName, exchange, ipoDate, delistedDate ) "
        "VALUES (%s, %s, %s, %s, %s)"
    )
    cursor.execute(
        add_hist_devidends,
        (
            data.symbol,
            data.companyName,
            data.exchange,
            data.ipoDate,
            data.delistedDate,
        ),
    )
    print(cursor.lastrowid)
    cnx.commit()
    cursor.close()
    cnx.close()
