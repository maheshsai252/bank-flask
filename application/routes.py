from application import app
from flask import render_template,flash,redirect,url_for,session
from application.forms import LoginForm,RegisterForm,AddCustomerForm,UpdateCustomerForm,UpdateCustomerFormUpdate,DeleteCustomerForm,AddAccountForm,GetAccounts
from application.models import User,Customer,Account,CustomerStatus,AccountStatus
from datetime import datetime

# Routes management in application

#home route
@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html")
#login route
@app.route("/login",methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():

        email       = form.email.data
        password    = form.password.data
        user = User.objects(email=email).first()
        print(email)
        if user and user.get_password(password):
            flash(f"{user.first_name}, you are successfully logged in!", "success")
            session['username'] = user.first_name

            if(user.get_role()=='customer'):
                session['role']='customer'
                return redirect(url_for('add_customer'))
            else:
                session['role']=''
                return redirect(url_for('get_accountsform'))
        else:
            flash("Sorry, something went wrong.","danger")
            return redirect(url_for('login'))
    return render_template("login/login.html", title="Login", form=form)
#register route
@app.route("/register", methods=['POST','GET'])
def register():
    # if session.get('username'):
    #     return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user_id     = User.objects.count()
        user_id     += 1

        email       = form.email.data
        password    = form.password.data
        first_name  = form.first_name.data
        last_name   = form.last_name.data

        role=form.role.data
        if User.objects(email=email):
            flash("You are already registered","danger")
            return redirect(url_for('login'))
        else:
            user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name,role=role)
            user.set_password(password)
            user.save()
            flash("You are successfully registered!","success")
            return redirect(url_for('login'))

    return render_template("login/register.html", title="Register", form=form)
#logout route
@app.route("/logout")
def logout():
    flash(f"{session.get('username')}, you are successfully logged out!", "success")

    session.pop('username',None)
    session.pop('role',None)
    return redirect(url_for('login'))

#add-customer route

@app.route("/addcustomer",methods=['POST','GET'])
def add_customer():
    form=AddCustomerForm()
    if not session.get('username'):
        return redirect(url_for('login'))
    if form.validate_on_submit():
        customer_id = (form.customer_ssid.data)
        customer_name = (form.customer_name.data)
        state=(form.state.data)
        age=form.age.data
        city=form.city.data
        address=form.address.data
        if Customer.objects(customer_ssid=customer_id):
            flash("already registered customer,update here..","danger")
            return redirect(url_for("update_customer"))

        customer = Customer(customer_ssid=customer_id,customer_name=customer_name,age=age,state=state,city=city,address=address)
        customer.save()
        customer_status=CustomerStatus(customer_ssid=customer_id,status="Created",message="customer created successfully",last_updated=(datetime.now()))
        customer_status.save()
        flash("successfully added customer","success")
        return redirect(url_for('add_customer'))

    return render_template("customer/add_customer.html",form=form,role=session.get('role'))
#update customer route

@app.route("/updatecustomer",methods=['POST','GET'])
def update_customer():
    form=UpdateCustomerForm()
    if not session.get('username'):
        return redirect(url_for('login'))
    if form.validate_on_submit():
        return redirect(url_for('update_customer_update',id=form.customer_ssid.data))




    return render_template("customer/update_customer.html",form=form,role=session.get('role'))
#delete customer route
@app.route("/deletecustomer",methods=['POST','GET'])
def delete_customer():
    form=DeleteCustomerForm()
    if not session.get('username'):
        return redirect(url_for('login'))
    if form.validate_on_submit():
        print("validated")
        Customer.objects(customer_ssid=form.customer_ssid.data).delete()
        customer_status=CustomerStatus(customer_ssid=form.customer_ssid.data,status="Deleted",message="customer deleted successfully",last_updated=(datetime.now()))
        customer_status.save()
        print(form.customer_ssid.data)
        return redirect(url_for('index'))




    return render_template("customer/delete_customer.html",form=form,title="Delete customer",role=session.get('role'))

#update details of customer in update customer page
@app.route("/updatecustomerupdate/<id>",methods=['POST','GET'])
def update_customer_update(id):

    form1=UpdateCustomerFormUpdate()
    if not session.get('username'):
        return redirect(url_for('login'))
    customer1 = Customer.objects(customer_ssid= id)
    customer=customer1[0]
    if form1.validate_on_submit():
        new_age= form1.age.data if form1.age.data !='' else customer['age']
        new_city=form1.city.data if form1.city.data !='' else customer['city']
        new_address=form1.address.data if form1.address.data !='' else customer['address']
        customer1.update(age=new_age)
        customer1.update(city=new_city)
        customer1.update(address=new_address)
        customer_status=CustomerStatus(customer_ssid=customer['customer_ssid'],status="updated",message="customer updated successfully",last_updated=(datetime.now()))
        customer_status.save()
        flash('updated successfully','success')
        return redirect(url_for('update_customer'))



    return render_template("customer/update_customer_update.html", customer_ssid=customer['customer_ssid'],customer_name=customer['customer_name'],age=customer['age'],state=customer['state'],city=customer['city'],address=customer['address'],form=form1,role=session.get('role'))
#status of customer

@app.route("/customerstatus")
def customer_status():
    data= CustomerStatus.objects.all()
    if not session.get('username'):
        return redirect(url_for('login'))

    return render_template("status/customer_status.html",data=data,role=session.get('role'))
#add-remaining routes

from application import account_routes
from application import account_transactions
