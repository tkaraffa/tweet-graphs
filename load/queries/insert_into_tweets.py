import sqlalchemy as sa


def query(**kwargs):
    query = sa.select(sa.func.generate_uuid().label("id"))
    return query
