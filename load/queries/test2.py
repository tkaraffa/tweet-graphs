import sqlalchemy as sa
from queries.tables import my_table


def query(**kwargs):
    query_object = sa.select(my_table.columns.one)
    return query_object
