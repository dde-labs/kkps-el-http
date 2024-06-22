import os

from dotenv import load_dotenv
import mysql.connector
from mysql.connector.errors import DatabaseError
from mysql.connector import errorcode

from models import HistDevidends, DelistedComps


load_dotenv()
TABLES: dict[str, str] = {
    'hist_devidends': (
        "CREATE TABLE `hist_devidends` ("
        "  `symbol` varchar(32) NOT NULL,"
        "  `date` date NOT NULL,"
        "  `label` varchar(16) NOT NULL,"
        "  `adjDividend` float NOT NULL,"
        "  `dividend` float  NOT NULL,"
        "  `recordDate` date NULL,"
        "  `paymentDate` date NULL,"
        "  `declarationDate` date NULL,"
        "  PRIMARY KEY (`symbol`, `date`)"
        ") ENGINE=InnoDB"
    ),
    'delisted_comp': (
        "CREATE TABLE `delisted_comp` ("
        "  `symbol` varchar(32) NOT NULL,"
        "  `companyName` varchar(256) NOT NULL,"
        "  `exchange` varchar(32) NOT NULL,"
        "  `ipoDate` date NOT NULL,"
        "  `delistedDate` date NOT NULL,"
        "  PRIMARY KEY (`symbol`)"
        ") ENGINE=InnoDB"
    ),
}


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


def create_tables():
    cnx = mysql.connector.connect(
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        host='127.0.0.1',
        database='db'
    )
    cursor = cnx.cursor()
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()
    cnx.close()


def insert_bulk_hist_devidends(all_data: HistDevidends):
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
    for data in all_data:
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
                data.declarationDate,
            ),
        )
        # break
    cnx.commit()
    cursor.close()
    cnx.close()


def insert_bulk_delisted_comp(all_data: DelistedComps):
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
    for data in all_data:
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
    cnx.commit()
    cursor.close()
    cnx.close()


if __name__ == '__main__':
    create_tables()
