#
#                          888       888                          888
#  e88~~\  d88~\ Y88b    / 888-~88e  888  e88~~8e  888-~88e  e88~\888
# d888    C888    Y88b  /  888  888b 888 d888  88b 888  888 d888  888
# 8888     Y88b    Y88b/   888  8888 888 8888__888 888  888 8888  888
# Y888      888D    Y8/    888  888P 888 Y888    , 888  888 Y888  888
#  "88__/ \_88P      Y     888-_88"  888  "88___/  888  888  "88_/888
#

"""Join or merge multiple CSVs.

Example::

    >>> from csvblend import MergeFiles
    >>> columns = ["a", "b", "c"]
    >>> indexes = ["a"]
    >>> with MergeFiles(columns, indexes) as mf:
    ...     with open(file1) as fp:
    ...         mf.merge(fp)
    ...     with open(file2) as fp:
    ...         mf.merge(fp)
    ...     with open(file3) as fp:
    ...         mf.merge(fp)
    ...     for row in mf.rows():
    ...         print(row)
"""

from csvblend.models import MergeFiles  # noqa: F401
