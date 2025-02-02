from app_contents.functions import *
from app_contents import app,session
from flask import render_template, redirect,request,url_for,flash, get_flashed_messages




@app.route('/login',methods=['POST','GET'])
def login_page():
     
      if(session.get("user")=="manager"):
           flash("You are already Logged in, Manager",category='normal-message')
      if request.method=='POST':
          e=request.form.get("email")
          p=request.form.get("password")
          if(e in getfromdb('email_add','users','uid')):
               l=getfromdb('email_add,uid','users','uid')
               for ele in l:
                   if(ele[0]==e):
                       uid=ele[1]

               if(p==getfromdbwhere('pwd','users','uid',f'uid={uid}')[0]):
                    session["user"]=uid
                    name=getfromdbwhere('fname','users','uid',f'uid={uid}')[0]
                    flash(f"You have successfully logged in! {name}",category='normal-message')
                    
                    return redirect(url_for('shop_page'))
            
               else:
                    flash("Please Enter the correct password",category='alert-message')
          else:
               flash("You have entered the wrong Email Address/Your account does not exist",category="alert-message")               
     
      return render_template('login.html')


@app.route('/register',methods=['POST','GET'])
def registration_page():  
  if request.method=='POST':
           flag=True
           e=request.form.get('email_add')
           p=request.form.get('pwd')
          
           if(request.form.get('email_add') in getfromdb('email_add','users','uid')):
                flash('An account with this email address already exists',category='alert-message')                
                flag=False                
           if(name_validate(request.form.get("fname"))!=True and flag):
                 k=name_validate(request.form.get("fname"))
                 flag=False
                 if(k=='length'):flash('Enter a proper name',category='alert-message')
                 if(k=='numb'):flash('Do not enter numbers in name',category='alert-message')
                 if(k=='special'):flash('Do not enter special characters in name',category='alert-message')
                 
                 
           if(is_valid_dob(request.form.get("dob"))==False and flag):
                flash('Please Input Proper Date of Birth',category='alert-message')
                flag=False
           if((is_valid_email(e))==False and flag):
                flash('Please Input Valid email address',category='alert-message')
                flag=False
           if(phone_num(request.form.get('phone_num')) and flag):
                flash('Please Input Valid Phone Number',category='alert-message')
                flag=False
           if(len(request.form.get('address'))<5 and flag) :
                flash('Please Input Valid address',category='alert-message')
                flag=False
           if(flag==True):     
               if(is_valid_pwd(p)=='length'):flash('The password is too short in length, Add more characters in it (8 characters minimum)',category='alert-message')
               if(is_valid_pwd(p)=='uppercase'):flash('The password has no capital letters, Add a capital letter in it',category='alert-message')
               if(is_valid_pwd(p)=='lowercase'):flash('The password has no lowercase (small) letters, Add a lowercase letter in it',category='alert-message')
               if(is_valid_pwd(p)=='number'):flash('The password does not contain any numeric digit, Add a numeric digit in it',category='alert-message')
               if(is_valid_pwd(p)=='special'): flash('The password does not contain any special character, Add a special character in it',category='alert-message')
               if(is_valid_pwd(p) and flag):
                    insert2db([request.form.get('fname'),request.form.get('dob'),e,request.form.get('phone_num'),request.form.get('address'),p],'users','uid')
                    flash("Your account has succesfully been registered",category='normal-message')
                    return redirect(url_for('login_page'))
        
  return render_template('register.html')


@app.route('/user_delete',methods=["POST","GET"])
def deletion_page():
    
    choice = request.form.get('choice')
    if choice == 'yes':
        k=delete_account(session["user"])
        if(k==True):
            flash("Your account has been deleted successfully",category='alert-message')
            session.pop("user")
            return redirect(url_for('home_page'))
    elif choice == 'no':
        return redirect(url_for('user_page'))
  
    return render_template('delete_page.html',data=getfromdbwhere('*','users','uid',f'uid={session["user"]}')[0])
    
    pass

@app.route('/user_page',methods=["POST","GET"])
def user_page():
     if(session.get("user")==None):
         flash('You need to Login first to access User Page','alert-message') 
         return redirect(url_for('login_page'))
     if(session.get("user")=="manager"):
         return redirect(url_for("manager"))
     if request.method=='POST':
           flag=True
           dictionary={}
           p=request.form.get('pwd')
         
           if(name_validate(request.form.get("fname"))!=True and len(request.form.get("fname"))>=1):
                 
                 k=name_validate(request.form.get("fname"))
                 flag=False
                 if(k=='length'):flash('Enter a proper name',category='alert-message')
                 if(k=='numb'):flash('Do not enter numbers in name',category='alert-message')
                 if(k=='special'):flash('Do not enter special characters in name',category='alert-message')
           if(name_validate(request.form.get("fname"))==True):
               dictionary["fname"]=request.form.get("fname")

           if(is_valid_dob(request.form.get("dob"))==False and flag and len(request.form.get("dob"))>=1):
                flash('Please Input Proper Date of Birth',category='alert-message')
                flag=False
           if(is_valid_dob(request.form.get('dob'))):
               dictionary["dob"]=request.form.get("dob")

           if(len(request.form.get('phone_num'))!=0 and phone_num(request.form.get('phone_num')) and flag):
                flash('Please Input Valid Phone Number',category='alert-message')
                flag=False
           if not(phone_num(request.form.get('phone_num'))):
              dictionary["phone_num"]=request.form.get("phone_num")
               
           if(len(request.form.get('address'))!=0 and len(request.form.get('address'))<5 and flag) :
                flash('Please Input Valid address',category='alert-message')
                flag=False
           if(not(len(request.form.get('address'))<5)) :
               dictionary["address"]=request.form.get("address")
    
           if(len(p)!=0):     
               if(is_valid_pwd(p)=='length'):flash('The password is too short in length, Add more characters in it (8 characters minimum)',category='alert-message')
               if(is_valid_pwd(p)=='uppercase'):flash('The password has no capital letters, Add a capital letter in it',category='alert-message')
               if(is_valid_pwd(p)=='lowercase'):flash('The password has no lowercase (small) letters, Add a lowercase letter in it',category='alert-message')
               if(is_valid_pwd(p)=='number'):flash('The password does not contain any numeric digit, Add a numeric digit in it',category='alert-message')
               if(is_valid_pwd(p)=='special'): flash('The password does not contain any special character, Add a special character in it',category='alert-message')
               if(is_valid_pwd(p)==True):
                   dictionary["pwd"]=request.form.get("pwd")
 
           
           if(dictionary!={}):
            u=update(dictionary,'users','uid',session["user"])
            flash('Details Successfully updated',category='normal-message')
            dictionary={}
           elif(flag and dictionary=={}):
               flash('No values entered',category='alert-message')       
      
     return render_template('user_page.html',data=getfromdbwhere('*','users','uid',f'uid={session["user"]}')[0])# data list "Page title"

@app.route('/logout')
def logout_page():
     
     if(session.get("user")==None):
          flash('You need to Login first to Logout ','alert-message') 
          return redirect(url_for('login_page'))
     elif(session.get("user")=="manager"):
      flash('You have been logged out successfully, Manager','alert-message')
      session.pop("user") 
     if(session.get("user")!=None):      
      name=getfromdbwhere('fname','users','uid',f'uid={session["user"]}')[0]       
      flash(f'You have been logged out succesfully, {name}','alert-message')
      session.pop("user") 
     
     return redirect(url_for('login_page'))







