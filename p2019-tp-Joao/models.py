from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase('my_database.db')
now = datetime.datetime.now

class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True) # Char field is a scalar variable (int, string, bool)
    password = CharField()
    phone = CharField()
    created_at = DateTimeField(default=now)
    updated_at = DateTimeField(default=now)
    is_deleted = BooleanField(default=False)


class Token(BaseModel):
    user_id = ForeignKeyField(User, related_name='token') # Foreign key to link the Token to related User
    login_token = CharField(unique=True)
    created_at = DateTimeField(default=now)


class Transaction(BaseModel):
    user_id = ForeignKeyField(User, related_name='transactions')
    amount = FloatField()
    created_at = DateTimeField(default=now)


class CodeLogin(BaseModel):
    user_id = ForeignKeyField(User, related_name='code_login')
    code = CharField(unique=True)
    created_at = DateTimeField(default=now)


class CodeTransaction(BaseModel):
    user_id = ForeignKeyField(User, related_name='code_transaction')
    code = CharField(unique=True)
    amount = CharField()
    charge_id = CharField()
    created_at = DateTimeField(default=now)


# Create tables with Peewee function
User.create_table(True)
Token.create_table(True)
Transaction.create_table(True)
CodeLogin.create_table(True)
CodeTransaction.create_table(True)

# Connect database with Peewee function
db.connect()
