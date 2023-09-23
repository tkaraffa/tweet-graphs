import sqlalchemy as sa

my_table = sa.Table("my_table", sa.MetaData(), sa.Column("one", sa.Integer))
