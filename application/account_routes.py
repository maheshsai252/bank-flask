
from application import app
from flask import render_template,flash,redirect,url_for,session
from application.forms import LoginForm,RegisterForm,AddCustomerForm,UpdateCustomerForm,UpdateCustomerFormUpdate,DeleteCustomerForm,AddAccountForm,GetAccounts,DeleteAccountForm
from application.models import User,Customer,Account,CustomerStatus,AccountStatus
from datetime import datetime

@app.route("/getaccountsform",methods=['GET','POST'])
def get_accountsform():
    form=GetAccounts()
    if form.validate_on_submit():
        id= form.customer_ssid.data
        flash(f"{session.get('username')}, you are having following accounts!", "success")
        return redirect(url_for('get_accounts',id= id))
    return render_template("account/getaccountsform.html",form=form,role=session.get('role'))

@app.route("/getaccounts/<id>",methods=['GET','POST'])
def get_accounts(id):
    data=Account.objects(customer_ssid=id).all()

    return render_template("account/get_accounts.html",role=session.get('role'),data=data)



@app.route("/getaccount/<id>",methods=['GET','POST'])
def get_account(id):
    data=Account.objects(account_id=id).first()
    return render_template("account/get_account.html",role=session.get('role'),data=data)


@app.route("/addaccount",methods=['POST','GET'])
def add_account():
    form=AddAccountForm()
    if form.validate_on_submit():
        customer_id = (form.customer_ssid.data)
        if(Customer.objects(customer_ssid=customer_id)):
            account_type = (form.account_type.data)
            amount=(form.amount.data)
            ac_id=Account.objects.count()
            ac_id+=1
            print(ac_id)
            customer = Account(customer_ssid=customer_id,account_id=ac_id,account_type=account_type,amount=amount)
            customer.save()

            flash("successfully added account","success")
            data= AccountStatus(customer_ssid=customer_id,account_id=ac_id,account_type=account_type,status="created",message="account created",last_updated=(datetime.now()))
            data.save()
            return redirect(url_for('add_account'))
        else:
            flash("no specified customer","danger")
    else:
        print(form.errors)
        print("not validated")
    return render_template("account/add_account.html",form=form,role=session.get('role'))



@app.route("/deleteaccount",methods=['POST','GET'])
def delete_account():
    form=DeleteAccountForm()
    if form.validate_on_submit():
        print(form.account_id.data)
        if(Account.objects(account_id=form.account_id.data).first()):
            obj = Account.objects(account_id=form.account_id.data).first()
        # print(obj[0]['customer_ssid'])
            data= AccountStatus(customer_ssid=obj['customer_ssid'],account_id=obj['account_id'],account_type=obj['account_type'],status="created",message="account created",last_updated=(datetime.now()))
            data.save()
            Account.objects(account_id=form.account_id.data).delete()
            flash("deleted successfully","success")
            return redirect(url_for('delete_account'))
        else:
            flash("not exist","danger")
            return redirect(url_for('delete_account'))


    else:
        print(form.errors)
        print("no")


    return render_template("account/delete_account.html",form=form,title="Delete account",role=session.get('role'))


@app.route("/accountstatus")
def account_status():
    data= AccountStatus.objects.all()
    return render_template("status/account_status.html",data=data,role=session.get('role'))
