from sqlalchemy import MetaData, Integer, String, Table, Column

metadata = MetaData()

words = Table(
    'words',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('word', String, nullable=False)
)

5