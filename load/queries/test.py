import sqlalchemy as sa

from queries.tables import my_table


def query(**kwargs):
    query_object = sa.insert(my_table).values(one=1)
    return query_object
