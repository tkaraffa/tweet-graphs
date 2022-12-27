import sqlalchemy as sa


def query(**kwargs):
    query_object = sa.select(
        [
            sa.func.generate_uuid().label("id"),
            sa.literal("test"),
            sa.literal(kwargs.get("test")),
            sa.literal(kwargs.get("test2")).label("blaaah"),
        ]
    )
    return query_object
