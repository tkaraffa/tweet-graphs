import os
from pathlib import Path
from sqlalchemy import text

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
    file_path = Path(filename)

    # make sure sql file exists
    if file_path.suffix not in (sql_suffix, ""):
        raise NotImplementedError(
            f"You used a {file_path.suffix} file. "
            + "Use either a stem or a .sql file!"
        )
    full_file_path = os.path.join(
        SQL_DIRECTORY, file_path.with_suffix(sql_suffix)
    )
    if not os.path.exists(full_file_path):
        raise FileNotFoundError(
            f"{full_file_path} does not exist!"
            + f"Check {SQL_DIRECTORY} for your file."
        )

    with open(full_file_path, "r") as f:
        query = text(f.read())
    return query
