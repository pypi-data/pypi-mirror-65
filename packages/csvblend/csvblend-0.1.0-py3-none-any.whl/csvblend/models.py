"""Primary objects that power csvblend."""

import contextlib
import csv
import logging
import os
import tempfile
import timeit

from csvblend import csvblend, utils

logger = logging.getLogger(__name__)


class MergeFiles(contextlib.AbstractContextManager):
    """Representation of a MergeFiles instance."""

    def __init__(self, columns, indexes, db=None):
        """Construct a new MergeFiles instance from a list of columns.

        :param list columns: The list of columns.
        :param list indexes: The list of indexes.
        :param str db: (optional) The database file database.
        """
        if not isinstance(columns, (list, tuple)):
            raise ValueError("columns should be a list or tuple")
        if not isinstance(indexes, (list, tuple)):
            raise ValueError("indexes should be a list or tuple")
        if not columns:
            raise ValueError("columns is an empty sequence")
        if not indexes:
            raise ValueError("indexes is an empty sequence")
        if not set(indexes).issubset(columns):
            raise ValueError("indexes must be a subset of columns")
        if len(columns) > len(set(columns)):
            raise ValueError("columns contains duplicate items")
        if len(indexes) > len(set(indexes)):
            raise ValueError("indexes contains duplicate items")
        # The number of rows affected by merge() (created or updated). This is not the
        # same as the number of rows in the merge table
        self.affected_count = 0
        # The number of rows in the merge table
        self.rowcount = 0
        # True if cleanup() has been called, otherwise False
        self.closed = False
        # The database parameter dict bindings
        self._columns = {utils.hash_function(i): i for i in columns}
        self._indexes = {utils.hash_function(i): i for i in indexes}
        # The database file database
        self._db = db
        # The underlying sqlite database connection
        self._connection = None
        # The database merge table
        self._table = "merge_table"
        # The number of times merge() has succeeded
        self._merge_count = 0

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the runtime context."""
        self.cleanup()

    def merge(self, csvfile):
        """Merge a csvfile into the merge CSV.

        :param object csvfile: Can be any object that returns a line of input
               for each iteration, such as a file object or a list.
        """
        if self.closed:
            raise ValueError("Operation on closed MergeFile")
        if not self._connection:
            if not self._db:
                self._db = os.path.join(tempfile.mkdtemp(), "merge_files.db")
            self._connection = csvblend.create_database(self._db)
            csvblend.create_table(
                self._connection, self._table, list(self._columns), list(self._indexes)
            )
        start_time = timeit.default_timer()
        reader = csv.DictReader(csvfile)
        # Hash the csvfile columns to match the (hashed) instance columns
        reader.fieldnames = [utils.hash_function(i) for i in reader.fieldnames]
        if not set(self._columns).issubset(reader.fieldnames):
            raise ValueError("fieldnames (csv header) must be a subset of columns")
        cursor = csvblend.insert_values(
            self._connection,
            self._table,
            list(self._columns),
            list(self._indexes),
            reader,
        )
        self._connection.commit()
        merge_time = timeit.default_timer()
        total_time = merge_time - start_time
        logger.debug("Merged csvfile in %ss", f"{total_time:.05f}")
        # affected_count is tracked relative to the first call to merge()
        if self._merge_count != 0:
            self.affected_count += cursor.rowcount
        self._merge_count += 1
        cursor = csvblend.count_values(self._connection, self._table)
        self.rowcount = cursor.fetchone()[0]

    def rows(self):
        """The returned object is an iterator.

        Each iteration returns a row of the merge CSV.

        :rtype: tuple
        """
        if self.closed:
            raise ValueError("Operation on closed MergeFile")
        if not self._connection:
            return
        cursor = csvblend.select_values(
            self._connection, self._table, list(self._columns)
        )
        for row in cursor:
            yield row

    def cleanup(self):
        """Cleanup the merge database."""
        if self.closed:
            return
        logger.debug("Called cleanup() on the instance")
        if self._connection:
            # Close the database connection
            self._connection.close()
            # Remove the database
            if self._db != ":memory:":
                os.remove(self._db)
        self.closed = True
