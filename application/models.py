import flask
from application import db
#User database
class User(db.Document):
    user_id     =   db.IntField( unique=True )
    first_name  =   db.StringField( max_length=50 )
    last_name   =   db.StringField( max_length=50 )
    email       =   db.StringField( max_length=30 )
    password    =   db.StringField( max_length=30 )
    role        =   db.StringField(max_length=20)
    def get_role(self):
        return self.role
    def set_password(self, password):
        self.password = (password)

    def get_password(self, password):
        # v= check_password_hash(self.password, password)

        return self.password == password
#customer status database
class CustomerStatus(db.Document):
    customer_ssid = db.IntField(max_length=9)
    status=db.StringField(max_length=10)
    message=db.StringField(max_length=100)
    last_updated=db.DateTimeField()
#account status collection
class AccountStatus(db.Document):
    customer_ssid = db.IntField(max_length=9)
    account_id = db.IntField(max_length=9)
    account_type=db.StringField(max_length=20)
    status=db.StringField(max_length=20)
    message=db.StringField(max_length=100)
    last_updated=db.DateTimeField()
#customer collection
class Customer(db.Document):
    customer_ssid = db.IntField(max_length=9)
    customer_name = db.StringField(max_length=30)
    age=db.IntField()
    address=db.StringField(max_length=100)
    state=db.StringField(max_length=30)
    city = db.StringField(max_length=30)

#account collection

class Account(db.Document):
    customer_ssid = db.IntField(max_length=9)
    account_id = db.IntField(max_length=9)
    account_type = db.StringField(max_length=30)
    amount=db.IntField(min_length=3)
    address=db.StringField(max_length=100)
    state=db.StringField(max_length=30)
    city = db.StringField(max_length=30)
    def set_id(self,accountid):
        self.account_id=accountid
    def get_id(self):
        return self.account_id
