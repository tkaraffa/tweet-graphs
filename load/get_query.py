import os
from pathlib import Path

SQL_DIRECTORY = os.path.join(os.path.dirname(__file__), "sql")


def get_query(filename: str) -> str:
    """
    Find a SQL file and return the string
    representation of its contents.

    Params
    ------
    filename: str
        The filename containing the SQL query to return

    Returns
    -------
    query: str
        The string representation of the query
    """

    sql_suffix = ".sql"
    if not filename.lower().endswith(sql_suffix):
        filename = Path(filename).with_suffix(sql_suffix)
    full_file_path = os.path.join(SQL_DIRECTORY, filename)
    print(full_file_path)
    with open(full_file_path, "r") as f:
        query = " ".join(line.strip("\n") for line in f.readlines())
    return query
