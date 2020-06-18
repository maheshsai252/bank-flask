from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,IntegerField,TextAreaField,SelectField,DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError,Optional
from application.models import User

#login form
class LoginForm(FlaskForm):
    email   = StringField("User Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6,max=15)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")
#register form
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

#add-customer form
class AddCustomerForm(FlaskForm):

    customer_ssid = StringField("Customer SSNID", validators=[DataRequired(),Length(min=9,max=9)])
    customer_name=StringField("Customer Name",validators=[DataRequired()])
    age=IntegerField("Age",validators=[DataRequired()])
    address = TextAreaField("Address",validators=[DataRequired()])
    state= SelectField("State",choices=[('ap','ap'),('ts','ts')],validators=[DataRequired()])
    city=StringField("City",validators=[DataRequired()])
    submit = SubmitField("Add Customer")
#update-customer form
class UpdateCustomerForm(FlaskForm):
    customer_ssid = StringField("Customer SSNID", validators=[DataRequired(),Length(min=9,max=9)])
    submit = SubmitField("Update Now")
#update with further details form
class UpdateCustomerFormUpdate(FlaskForm):

    age=IntegerField("New Age")
    address = TextAreaField(" New Address")
    city=StringField("New City")
    submit = SubmitField("Update Now")
#delete customer form
class DeleteCustomerForm(FlaskForm):
    customer_ssid = StringField("Customer SSNID", validators=[DataRequired(),Length(min=9,max=9)])
    submit = SubmitField("Delete Now")
#delete account form
class DeleteAccountForm(FlaskForm):
    account_id = StringField("Account ID", validators=[DataRequired(),Length(max=9)])
    submit = SubmitField("Delete Now")
#add-account form
class AddAccountForm(FlaskForm):

    customer_ssid = StringField("Customer SSNID", validators=[DataRequired(),Length(min=9,max=9)])
    account_type= SelectField("State",choices=[('savings','savings'),('current','current')],validators=[DataRequired()])
    amount=IntegerField("Amount",validators=[DataRequired()])
    submit = SubmitField("Add Account")
#get-accounts form
class GetAccounts(FlaskForm):
        customer_ssid = StringField("Customer SSNID", validators=[DataRequired(),Length(min=9,max=9)])
        submit = SubmitField("Get Accounts")
#get-statement form
class GetStatement(FlaskForm):
        account_id = StringField("Account ID", validators=[DataRequired(),Length(max=9)])
        number = IntegerField("Number of Transactions",validators=[Optional()])
        start_date = DateField('Start Date',validators=[Optional()])
        end_date = DateField('End Date',validators=[Optional()])
        submit = SubmitField("Get statement")
#Transaction debit and credit form
class AccountTransact(FlaskForm):
        customer_ssid = StringField("Customer SSNID", validators=[DataRequired(),Length(min=9,max=9)])
        account_id=StringField("Account ID", validators=[DataRequired(),Length(max=9)])
        amount=IntegerField("Amount",validators=[DataRequired()])
        submit = SubmitField("Transact")

#transfer form account to account
class AmountTransfer(FlaskForm):
        from_customer_ssid = StringField("From customer ssn id", validators=[DataRequired(),Length(min=9,max=9)])
        from_account_id=StringField("From Account id", validators=[DataRequired(),Length(max=9)])
        from_amount=IntegerField("To be transferred amount",validators=[DataRequired()])
        to_customer_ssid = StringField("To customer ssn id", validators=[DataRequired(),Length(min=9,max=9)])
        to_account_id=StringField("To Account id", validators=[DataRequired(),Length(max=9)])
        submit = SubmitField("Transfer")
