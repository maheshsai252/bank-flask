from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,IntegerField,TextAreaField,SelectField,DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError,Optional
from application.models import User


class LoginForm(FlaskForm):
    email   = StringField("User Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6,max=15)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    email   = StringField("User Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(),Length(min=6,max=15)])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(),Length(min=6,max=15), EqualTo('password')])
    first_name = StringField("First Name", validators=[DataRequired(),Length(min=2,max=55)])
    last_name = StringField("Last Name", validators=[DataRequired(),Length(min=2,max=55)])
    role = SelectField("Select your role",choices=[('customer','customer'),('cashier','cashier')],validators=[DataRequired()])
    submit = SubmitField("Register Now")

    def validate_email(self,email):
        user = User.objects(email=email.data).first()
        if user:
            raise ValidationError("Email is already in use. Pick another one.")


class AddCustomerForm(FlaskForm):

    customer_ssid = StringField("customer ssn id", validators=[DataRequired(),Length(min=9,max=9)])
    customer_name=StringField("customer name",validators=[DataRequired()])
    age=IntegerField("age",validators=[DataRequired()])
    address = TextAreaField("address",validators=[DataRequired()])
    state= SelectField("state",choices=[('ap','ap'),('ts','ts')],validators=[DataRequired()])
    city=StringField("city",validators=[DataRequired()])
    submit = SubmitField("Add Customer")

class UpdateCustomerForm(FlaskForm):
    customer_ssid = StringField("customer ssn id", validators=[DataRequired(),Length(min=9,max=9)])
    submit = SubmitField("update Now")
class UpdateCustomerFormUpdate(FlaskForm):

    age=IntegerField("new age")
    address = TextAreaField(" new address")
    city=StringField("new city")
    submit = SubmitField("Register Now")

class DeleteCustomerForm(FlaskForm):
    customer_ssid = StringField("customer ssn id", validators=[DataRequired(),Length(min=9,max=9)])
    submit = SubmitField("Delete Now")
class DeleteAccountForm(FlaskForm):
    account_id = StringField("Account id", validators=[DataRequired(),Length(max=9)])
    submit = SubmitField("Delete Now")

class AddAccountForm(FlaskForm):

    customer_ssid = StringField("customer ssn id", validators=[DataRequired(),Length(min=9,max=9)])
    account_type= SelectField("state",choices=[('savings','savings'),('current','current')],validators=[DataRequired()])
    amount=IntegerField("amount",validators=[DataRequired()])
    submit = SubmitField("Add Account")

class GetAccounts(FlaskForm):
        customer_ssid = StringField("customer ssn id", validators=[DataRequired(),Length(min=9,max=9)])
        submit = SubmitField("Get Accounts")

class GetStatement(FlaskForm):
        account_id = StringField("account id", validators=[DataRequired(),Length(max=9)])
        number = IntegerField("number",validators=[Optional()])
        start_date = DateField('Start Date',validators=[Optional()])
        end_date = DateField('End Date',validators=[Optional()])
        submit = SubmitField("Get statement")
class AccountTransact(FlaskForm):
        customer_ssid = StringField("customer ssn id", validators=[DataRequired(),Length(min=9,max=9)])
        account_id=StringField("Account id", validators=[DataRequired(),Length(max=9)])
        amount=IntegerField("amount",validators=[DataRequired()])
        submit = SubmitField("Transact")

class AmountTransfer(FlaskForm):
        from_customer_ssid = StringField("from customer ssn id", validators=[DataRequired(),Length(min=9,max=9)])
        from_account_id=StringField("from Account id", validators=[DataRequired(),Length(max=9)])
        from_amount=IntegerField("to be transferred amount",validators=[DataRequired()])
        to_customer_ssid = StringField("to customer ssn id", validators=[DataRequired(),Length(min=9,max=9)])
        to_account_id=StringField("to Account id", validators=[DataRequired(),Length(max=9)])
        submit = SubmitField("Transfer")
