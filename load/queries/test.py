import sqlalchemy as sa


def query(**kwargs):
    query = sa.select(
        [
            sa.func.generate_uuid().label("id"),
            sa.literal(kwargs.get("test")),
        ]
    )
    return query
