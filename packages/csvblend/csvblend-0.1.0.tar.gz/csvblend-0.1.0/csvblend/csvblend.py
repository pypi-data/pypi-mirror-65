"""Primary methods that power csvblend."""

import logging
import sqlite3

logger = logging.getLogger(__name__)


def create_database(database):
    """Create a merge database (SQLite3).

    :param str database: The database file.
    :rtype: sqlite3.Connection
    """
    logger.debug("Create the merge database: '%s'", database)
    connection = sqlite3.connect(database)
    # Disable the rollback journal completely
    connection.execute("PRAGMA journal_mode = OFF;")
    # Change the "synchronous" flag to OFF
    connection.execute("PRAGMA synchronous = OFF;")
    return connection


def create_table(connection, table, columns, indexes):
    """Create a merge database table.

    :param sqlite3.Connection connection: The database connection.
    :param str table: The merge table.
    :param list columns: The table columns.
    :param list indexes: The table indexes.
    :rtype: sqlite3.Cursor
    """
    create_columns = ", ".join([f'"{i}" TEXT' for i in columns])
    create_indexes = ", ".join([f'"{i}"' for i in indexes])
    query = f"""
        CREATE TABLE {table} ({create_columns},
        UNIQUE ({create_indexes}));
    """
    logger.debug("Create the merge table")
    return connection.execute(query)


def insert_values(connection, table, columns, indexes, values):
    """Insert values into a merge table.

    :param sqlite3.Connection connection: The database connection.
    :param str table: The merge table.
    :param list columns: The table columns.
    :param list indexes: The table indexes.
    :param list[tuple] values: The values to insert.
    :rtype: sqlite3.Cursor
    """
    insert_columns = ", ".join([f'"{i}"' for i in columns])
    insert_indexes = ", ".join([f'"{i}"' for i in indexes])
    insert_bindings = ", ".join([f"@{i}" for i in columns])
    query = f"""
        INSERT INTO {table} ({insert_columns})
        VALUES ({insert_bindings})
        ON CONFLICT ({insert_indexes})
    """
    # The table indexes value columns (columns - indexes)
    ivalues = [i for i in columns if i not in indexes]
    if ivalues:
        update_columns = ", ".join([f'"{i}"' for i in ivalues])
        update_bindings = ", ".join([f"@{i}" for i in ivalues])
        # The idea of the UPSERT statement is that when a UNIQUE or PRIMARY KEY
        # constraint violation occurs, the UPSERT statement:
        # - First, checks if the existing row that causes the constraint
        #   violation matches the new row
        # - Second, if no match, updates the existing row values with the new
        #   row
        query += f"""
            DO UPDATE SET ({update_columns}) = ({update_bindings})
            WHERE ({update_columns}) != ({update_bindings})
        """
    else:
        query += f"""
            DO NOTHING
        """
    query += ";"
    logger.debug("Insert the merge values")
    return connection.executemany(query, values)


def select_values(connection, table, columns):
    """Select the values from a merge table.

    :param sqlite3.Connection connection: The database connection.
    :param str table: The merge table.
    :param list columns: The table columns.
    :rtype: sqlite3.Cursor
    """
    select_columns = ", ".join([f'"{i}"' for i in columns])
    query = f"""
        SELECT {select_columns} FROM {table};
    """
    logger.debug("Select the merge values")
    return connection.execute(query)


def count_values(connection, table):
    """Count the values inside a merge table.

    :param sqlite3.Connection connection: The database connection.
    :param str table: The merge table.
    :rtype: sqlite3.Cursor
    """
    query = f"""
        SELECT count(*) FROM {table};
    """
    logger.debug("Count the merge values")
    return connection.execute(query)
