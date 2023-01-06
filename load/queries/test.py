import sqlalchemy as sa


def query(**kwargs):
    query_object = sa.select(
        [
            sa.func.generate_uuid().label("id"),
            sa.literal("test"),
        ]
    )
    return query_object
