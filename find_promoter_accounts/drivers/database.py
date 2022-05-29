import sqlalchemy
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, Boolean, create_engine, TIMESTAMP, Numeric, DATE
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker

Base = declarative_base()

class Database():

    def __init__(self, database_name, table_names):
        self.connection = None
        self.counter = 0
        self.database_name = database_name
        if len(table_names) == 0:
            self.tables = Base.metadata.tables.values()
        else:
            self.tables = []
            for table_name in table_names:
                self.tables.append(Base.metadata.tables[table_name])
        self.table_rows = []
        self.all_inserted_rows = {}
        Database.db_name = database_name
        self.url = None

    def create_database_connection(self, database_url):
        self.url = database_url
        self.engine = sqlalchemy.create_engine(database_url + self.database_name)
        Base.metadata.create_all(self.engine, tables=self.tables, checkfirst=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_table_size(self, table):
        return self.session.query(table).count()

    def insert_into_table(self, table, table_rows):
        entries_inserted_successfully = -1
        if len(table_rows) > 0:
            # Commit the record the database
            try:
                insert_query = insert(table).values(table_rows).on_conflict_do_nothing()
                self.session.execute(insert_query)
                self.session.commit()
                entries_inserted_successfully = len(table_rows)
            except:
                print('Failed inserting into table')
                self.session.rollback()
            finally:
                self.session.close()

        return entries_inserted_successfully
    
    def insert_object_into_table(self, obj):
        try:
            self.session.add(obj)
            self.session.commit()
        except sqlalchemy.exc.IntegrityError as ie:
            print(ie.orig.pgerror.split('DETAIL:')[-1].strip())
            self.session.rollback()
        except:
            printexception('Failed inserting into table')
            self.session.rollback()
        finally:
            self.session.close()

class Asset(Base):
    column1 = Column('column1', Text, primary_key=True)
    column2 = Column('column2', Text, primary_key=True)
    column3 = Column('column3', Text)
    id = Column('id', Integer)

    def __init__(self, column1, column2, column3):
        self.column1 = column1
        self.column2 = column2
        self.column3 = column3
