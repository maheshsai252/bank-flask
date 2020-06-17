from application import app
from flask import render_template,flash,redirect,url_for,session
import mongoengine as me
from application.forms import AccountTransact,AmountTransfer,GetStatement

from application.models import User,Customer,Account,CustomerStatus,AccountStatus

from datetime import datetime

@app.route("/debit",methods=['GET','POST'])
def debit():
    form=AccountTransact()
    if form.validate_on_submit():
        customer_id = form.customer_ssid.data
        account_id = form.account_id.data
        amount = form.amount.data
        account = Account.objects(customer_ssid=customer_id,account_id=account_id).first()
        oldamount= account['amount']
        if(oldamount >= amount and amount>0 ):
            account.update(amount=(oldamount-amount))
            data= AccountStatus(customer_ssid=customer_id,account_id=account_id,account_type=account['account_type'],status="debited",message=f"Rs.{amount} debited from account",last_updated=(datetime.now()))
            data.save()
            print((oldamount-amount))
            flash(f"{session.get('username')}, {amount} debited from your account !", "success")
            return redirect(url_for('get_account',id=account_id))
        else:
            flash(f"{session.get('username')}, enter valid amount, not this {amount}!", "danger")
            return(redirect(url_for('debit')))
    return render_template('account/debit.html',form=form,role=session.get('role'),title="Debit Transaction")

@app.route("/credit",methods=['GET','POST'])
def credit():
    form=AccountTransact()
    if form.validate_on_submit():
        customer_id = form.customer_ssid.data
        account_id = form.account_id.data
        amount = form.amount.data
        account = Account.objects(customer_ssid=customer_id,account_id=account_id).first()
        oldamount= account['amount']
        if(amount>0 ):
            account.update(amount=(oldamount+amount))

            data= AccountStatus(customer_ssid=customer_id,account_id=account_id,account_type=account['account_type'],status="credited",message=f"Rs.{amount} credited to account",last_updated=(datetime.now()))
            data.save()
            flash(f"{session.get('username')},{amount} credited to your account !", "success")
            return redirect(url_for('get_account',id=account_id))
        else:
            flash(f"{session.get('username')},  enter valid amount, not this {amount}!", "danger")
            return(redirect(url_for('debit')))
    return render_template('account/debit.html',form=form,role=session.get('role'),title="Cedit Transaction")



@app.route("/transfer",methods=['GET','POST'])
def transfer():
    form=AmountTransfer()
    if form.validate_on_submit():
        customer_id = form.from_customer_ssid.data
        account_id = form.from_account_id.data
        amount = form.from_amount.data
        account1 = Account.objects(customer_ssid=customer_id,account_id=account_id).first()
        old_amount1=account1['amount']

        to_customer_id = form.to_customer_ssid.data
        to_account_id = form.to_account_id.data
        account2 = Account.objects(customer_ssid=to_customer_id,account_id=to_account_id).first()
        old_amount2=account2['amount']
        if(old_amount1 > amount and amount>0 and account_id!=to_account_id):
            flash(f"{session.get('username')}, transaction of {amount} is completed !", "success")
            t1=(old_amount1-amount)
            account1.update(amount=t1)
            t2=(old_amount2+amount)
            account2.update(amount=t2)
            print(old_amount1-amount)
            data= AccountStatus(customer_ssid=customer_id,account_id=account_id,account_type=account1['account_type'],status="debited",message=f"Rs.{amount} debited from account",last_updated=(datetime.now()))
            data.save()
            data1= AccountStatus(customer_ssid=to_customer_id,account_id=to_account_id,account_type=account2['account_type'],status="credited",message=f"Rs.{amount} credited to account",last_updated=(datetime.now()))
            data1.save()
            return render_template('account/transfer_after.html',role=session.get('role'),data1=account1,data2=account2,amount=amount,amount1=t1,amount2=t2)
        else:
            flash(f"{session.get('username')},  enter valid amount, not this {amount}!", "danger")
            return redirect(url_for('transfer'))

    return render_template('account/transfer.html',role=session.get('role'),form=form,title="Transfer Amount")






@app.route("/accountstatusform",methods=['POST','GET'])
def account_status_form():

    form=GetStatement()
    if form.validate_on_submit():
        id=form.account_id.data
        n=form.number.data
        start=(form.start_date.data)
        end=(form.end_date.data)
        if(n):
            data= AccountStatus.objects(account_id=id).order_by('-last_updated')[:n]
        else:
            data= AccountStatus.objects(account_id=id).filter((me.Q(last_updated__gte=start) & me.Q(last_updated__lte=end)))
        #print(data[0]['last_updated'].date())
        return render_template("status/account_status.html",data=data,role=session.get('role'))
    return render_template("status/statement.html",role=session.get('role'),form=form)
