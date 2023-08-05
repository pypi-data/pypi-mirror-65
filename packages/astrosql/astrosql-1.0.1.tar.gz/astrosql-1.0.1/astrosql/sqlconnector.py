import os
import getpass
from peewee import *  # very unfortunate to import all, blame the peewee legacy code

DBMS = str.lower(os.environ.get("ASTROSQL_DBMS", "mysql"))


def connect(database, dbms=DBMS, *args, **kwargs):
    """
    Args:
        database (str): Database name in SQL.
        dbms (str, optional): The DataBase Management System to be used. Currenly MySQL is only supported. Defaults to environment variable ASTROSQL_DBMS.
    """
    if dbms == "mysql":
        return pymysql_connect(database, *args, **kwargs)
    elif dbms == "postgresql":
        raise NotImplementedError(
            "Only MySQL supported, if you'd like to use PostgreSQL please make an issue at https://github.com/ketozhang/astroSQL/issues"
        )
    else:
        raise NotImplementedError(
            'Only MySQL supported, please set ASTROSQL_DBMS to "mysql" or leave it blank.'
        )


def pymysql_connect(database, read_default_file="~/.my.cnf", **kwargs):
    """
    Args:
        database (str): Database name in SQL.
        read_default_file (str):  Path to cnf file to be read. The [client] will be read for login credentials. Defaults to "~/.my.cnf".
        **kwargs: Directly passed to MySQLDatabase, a peewee wrapper for the pymysql interface (see https://pymysql.readthedocs.io/en/latest/modules/connections.html for more options). If specified, `read_default_file` configuration will be ignored.
            user (str, optional)
            password (str, optional)
            host (str, optional): Host name or IP. Defaults to "localhost"
    Returns:
        MySQLDatabase: An instance of MySQL database (peewee.MySQLDatabase).
    """
    # if not user or not password:
    #     user = input("Username: ")
    #     password = getpass.getpass()
    return MySQLDatabase(
        database=database, read_default_file=read_default_file, **kwargs
    )
