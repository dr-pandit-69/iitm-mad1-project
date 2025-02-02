from app_contents.functions import *
from app_contents import app
from flask import render_template, redirect, session,request,url_for,flash, get_flashed_messages
from random import randint
from PIL import Image


@app.route('/manager', methods=['POST','GET'])
def manager():
     category=getfromdb_as_dict('*','category','c_id')
     category1={}
     for ele in category:
          category1[ele['c_id']]=ele['category_name']


     products=getfromdb_as_dict('*','items','i_id')
     for product in products:
          
          if(product['c_id'] in category1.keys()):
               product['category']=category1[product['c_id']]
     if(session.get("user")!="manager"):
          flash("You need to login, Mr Manager!",category='alert-message')
          return redirect(url_for('manager_page'))
    
     if(len(products)>5):
          n=5
     else:
          n=len(products)

     transac={}
     t=getfromdb_as_dict('*','transactions','tid')
     print(t)
     t_avg=0
     count=[]
     items={}     
     for ele in t:
          t_avg+=ele['t_total']
          count.append(ele['uid'])
          items_dict = eval(ele['items'])
          for key in items_dict.keys():
               if(key not in items.keys()):
                    items[key]=items_dict[key]
               else:
                    items[key]+=items[key]+items_dict[key]

     Key_max = max(zip(items.values(), items.keys()))[1]
     transac['item']=getfromdbwhere('Name','items','iid',f'iid={Key_max}')[0]                


     max1=max(count, key=count.count)
     if(max1==-1):
          transac['custom']="Manager"
     else:
          transac['custom']=getfromdbwhere('fname','users','uid',f'uid={max1}')[0]          

     
     
     transac['count']=len(t)
     transac['avg']=int(t_avg/len(t))   
      






     return render_template('manager.html',category=category,products=products[0:n],transac=transac)



@app.route('/mgmt_cat')
def mgmt_cat():
     category=getfromdb_as_dict('*','category','c_id')

     return render_template('management_cat.html', category=category)

@app.route('/mgmt_prod')
def mgmt_prod():
     category=getfromdb_as_dict('*','category','c_id')
     products=getfromdb_as_dict('*','items','i_id')
     category1={}
     for ele in category:
          category1[ele['c_id']]=ele['category_name']

     for product in products:
          
          if(product['c_id'] in category1.keys()):
               product['category']=category1[product['c_id']]
     if(session.get("user")!="manager"):
          flash("You need to login, Mr Manager!",category='alert-message')
          return redirect(url_for('manager_page'))
    
    

     return render_template('management_prod.html',products=products)



@app.route('/add_category', methods=['POST','GET'])
def add_category():
     if request.method=='POST':
          if(name_validate(request.form.get('name'))!=True):
               k=name_validate(request.form.get("name"))
               if(k=='length'):flash('Enter a proper name',category='alert-message')
               if(k=='numb'):flash('Do not enter numbers in name',category='alert-message')
               if(k=='special'):flash('Do not enter special characters in name',category='alert-message')
          if(name_validate(request.form.get('name'))==True):
               if(request.form.get('name') in getfromdb('category_name','category','c_id')):
                    flash('This category already exists',category='alert-message')
               else:
                    insertcat2table(request.form.get('name'))
                    flash('Category has been added',category='normal-message')
                    return redirect(url_for('manager'))

     return render_template('add_category.html')           


@app.route('/edit_category/<id>', methods=['POST','GET'])
def edit_category(id):
     c=getfromdbwhere_as_dict('*','category','c_id',f'c_id={id}')[0]
     if request.method=='POST':
          if(name_validate(request.form.get('name'))!=True):
               k=name_validate(request.form.get("name"))
               if(k=='length'):flash('Enter a proper name',category='alert-message')
               if(k=='numb'):flash('Do not enter numbers in name',category='alert-message')
               if(k=='special'):flash('Do not enter special characters in name',category='alert-message')
          if(name_validate(request.form.get('name'))==True):
             
               
                    modcat(id,request.form.get('name'))
                    flash('Category has been modified',category='normal-message')
                    return redirect(url_for('mgmt_cat'))

     return render_template('edit_category.html',category=c)     


@app.route('/delete_cat/<id>')
def delete_cat(id):
     deletecat(id)
     flash('the category has been deleted',category='alert-message')
     return redirect(url_for('mgmt_cat'))

   

@app.route('/add_product',methods=['POST','GET'])
def add_product():
     flag=True

     category=getfromdb_as_dict('*','category','c_id')
     category1={}
     for ele in category:
          category1[ele['c_id']]=ele['category_name']

     if request.method=='POST':
             
           if(name_validate(request.form.get('name'))!=True):
               k=name_validate(request.form.get("name"))
               if(k=='length'):flash('Enter a proper name',category='alert-message')
               if(k=='numb'):flash('Do not enter numbers in name',category='alert-message')
               if(k=='special'):flash('Do not enter special characters in name',category='alert-message')
               flag=False
           
           if((request.form.get('qty')).isnumeric()==False and flag):
                flash('Enter valid Quantity',category='alert-message')
                flag=False  
           if((request.form.get('price')).isnumeric()==False and flag):
                flash('Enter valid price',category='alert-message')
                flag=False
           if(flag==True):
                pass
                l=[]
                l.append(request.form.get('name'))
                l.append(request.form.get('price')) 
                l.append(randint(100000000000,900000000000))
                l.append(request.form.get('description')) 
                l.append(request.form.get('qty')) 
                l.append(request.form.get('units')) 
                l.append(request.form.get('c_id'))
                l.append(request.form.get('name')+request.form.get('description'))
                uploaded_file = request.files['image']
                if uploaded_file.filename!='':
                   l.append(request.form.get('exp_date'))   
                   l.append(uploaded_file)
                   insertprod2table(l)
                   print(l)
                   flash('Product has been added succesfully', category='normal-message')
                else:
                     flash('Upload a valid image', category='alert-message') 


   
     return render_template('add_product.html',cat_list=category1)


@app.route('/edit_product/<id>', methods=['POST','GET'])
def edit_product(id):
     category=getfromdb_as_dict('*','category','c_id')

     category1={}
     for ele in category:
          category1[ele['c_id']]=ele['category_name']

      
     p=getfromdbwhere_as_dict('*','items','iid',f'iid={id}')[0]
     

     if request.method=='POST':
          flag=True
          update_keys={}
          for key in request.form.keys():
          
           if(request.form[key]!=''):
               
               f1=True

               if(key=='name' and name_validate(request.form.get('name'))!=True):
                 k=name_validate(request.form.get("name"))
                 if(k=='length'):flash('Enter a proper name',category='alert-message')
                 if(k=='numb'):flash('Do not enter numbers in name',category='alert-message')
                 if(k=='special'):flash('Do not enter special characters in name',category='alert-message')
                 flag=False
                 f1=False
                 

               if(key=='qty' and (request.form.get('qty')).isnumeric()==False and flag):
                flash('Enter valid Quantity',category='alert-message')
                flag=False 
                f1=False
                

               if(key=='price' and (request.form.get('price')).isnumeric()==False and flag):
                  flash('Enter valid price',category='alert-message')
                  flag=False
                  f1=False
                  
              
               if(f1==True):
                    print("YEY")
                    if(key in ['qty','price','c_id']):
                     update_keys[key]=int(request.form[key])
                    else:
                     update_keys[key]=(request.form[key])

          
          if(update_keys['c_id']==p['c_id']):
              update_keys.pop('c_id')

          print(update_keys)

          if(request.files['image'].filename!=''):
                    updateimage(request.files['image'],p['i_id'])

          if(update_keys!={}):
           update_item_columns(id,update_keys)
           flash('Values updated successfully',category='normal-message')
           return redirect(url_for('mgmt_prod'))
          else:
               flash('Enter Any Value',category='alert-message')

                     

     return render_template('edit_product.html',product=p,cat_list=category1)    


@app.route('/delete_prod/<id>')
def delete_prod(id):

     deleteprod(id)
     flash('the Product has been deleted',category='alert-message')

     return redirect(url_for('mgmt_prod'))

 
@app.route('/login_manager', methods=['POST','GET'])
def manager_page():   
         
      if(session.get("user")=="manager"):
           flash("You are already Logged in, Manager",category='normal-message')
      if request.method=='POST':
          e=request.form.get("email")
          p=request.form.get("password")
          if(e in getfromdb('email_add','manager','mid')):
               l=getfromdb('email_add,mid','manager','mid')
               for ele in l:
                   if(ele[0]==e):
                       mid=ele[1]

               if(p==getfromdbwhere('pwd','manager','mid',f'mid={mid}')[0]):
                    session["user"]='manager'
                    name=getfromdbwhere('fname','manager','mid',f'mid={mid}')[0]
                    flash(f"You have successfully logged in! Manager {name}",category='normal-message')
                    
                    return redirect(url_for('manager'))
            
               else:
                    flash("Please Enter the correct password",category='alert-message')
          else:
               flash("You have entered the wrong Email Address/Your account does not exist",category="alert-message")               
     
      

      return render_template('manager_login.html')



@app.route('/new_manager', methods=["POST","GET"])
def new_manager():
      if request.method=='POST':
           flag=True
           e=request.form.get('email_add')
           p=request.form.get('pwd')

           if(request.form.get('pin')!='1234'):
                flash('The Secret Access Pin is incorrect',category='alert-message') 
                flag=False
           
           if(request.form.get('email_add') in getfromdb('email_add','users','uid') and flag):
                flash('An account with this email address already exists',category='alert-message')                
                flag=False                
           if(name_validate(request.form.get("fname"))!=True):
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
                    insert2db1([request.form.get('fname'),request.form.get('dob'),e,request.form.get('phone_num'),request.form.get('address'),p],'manager','mid')
                    flash("Your manager account has succesfully been registered",category='normal-message')
                    return redirect(url_for('manager_page'))

      return render_template('new_manager.html')   



