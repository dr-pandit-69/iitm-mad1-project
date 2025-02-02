from app_contents.functions import *
from app_contents import app
from flask import render_template, redirect,request,url_for,flash, get_flashed_messages
import random
from app_contents import session
import requests

@app.route('/')
@app.route('/home')
def home_page():
     if(session.get('user')==None):
          flash('Please Login/ Create an account to acccess our store :D','alert-message')
        
          return redirect(url_for('login_page'))
     
     try:
      
      if(session['user']==None):
        return redirect(url_for('login_page'))
     except:
       return redirect(url_for('login_page'))
     
     
     categories = getfromdb_as_dict('c_id, category_name', 'category', 'c_id')
     products = {}

     
     featured=[]  

     for elem in categories:
        c_id=(elem['c_id'])
        p=getfromdbwhere_as_dict('*','items','iid',f'c_id={c_id}')
    
        q=[]
        for ele in p:         
            newele=ele
            newele['image']=get_image_for_item(ele['i_id'])
            q.append(newele)
        
        if(len(q)>0 and len(featured)<=4):
         featured.append(q[random.randint(0,len(q)-1)])
        
        if(len(q)>=4):
           q=q[0:4]
        products[c_id]=q      
     

        

     return render_template('home.html',categories=categories,products=products,featured=featured)



@app.route('/shop')

def shop_page():
    try:
      if(session['user']==None):
        return redirect(url_for('login_page'))
    except:
       return redirect(url_for('login_page'))
         
    categories = getfromdb_as_dict('c_id, category_name', 'category', 'c_id')
    products = {}

    for elem in categories:
        c_id=(elem['c_id'])
        p=getfromdbwhere_as_dict('*','items','iid',f'c_id={c_id}')
        q=[]
        for ele in p:         
            newele=ele
            newele['image']=get_image_for_item(ele['i_id'])
            q.append(newele)

        products[c_id]=q 
        
   
    return render_template('shop.html', categories=categories, products=products)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    flag=True
    try:
     if(session["user"]==None and session["manager"]==None):
        return redirect(url_for('login_page'))
    except KeyError:
        return redirect(url_for('login_page'))
    
    if 'cart' not in session:
        session['cart'] = {}  
    cart = session['cart']
  
    item_id = str(request.form['i_id'])
    
    quantity = int(request.form['quantity'])
    existing_qty=getfromdbwhere('qty','items','iid',f'iid={int(item_id)}')[0]
    q=0

    if(item_id in session['cart'].keys()):
       q=session['cart'][item_id]

      
    if(q+quantity>existing_qty):
       flash(f'Enter a quantity lower than {existing_qty-q}',category='alert-message')
       flag=False
       return redirect(url_for('shop_page'))
  
  
    if item_id in cart.keys() and flag:
        cart[item_id]=int(cart[item_id])+quantity 
        pass 
    elif(flag):
       cart[item_id]=quantity   
    
    flash('Item added to cart successfully', 'normal-message')
   
    return redirect(url_for('shop_page'))





@app.route('/cart',methods=['POST','GET'])
def cart_page():
    try:
      if(session['user']==None):
        return redirect(url_for('login_page'))
    except:
       return redirect(url_for('login_page'))
    flash('Use the code FIRSTORDER10 to get 10 percent off on your order',category='normal-message')
    
    cart = session.get('cart', {})
   
    cart_items = []

    for key in cart.keys():

     k=(getfromdbwhere_as_dict1(int(key)))
     k['quantity']=cart[key]
     cart_items.append(k)

   
    total_price=0

    for item in cart_items:
        total_price+=item['price']*item['quantity']

    if request.method=='POST':
          
       return redirect(url_for('checkout_page',total=total_price,coupon=request.form["coupon"]))
       


    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


@app.route('/checkout/<total>')
def checkout_page(total,coupon=0):   
        try:
       
         if(coupon=='FIRSTORDER10' and int(session['user']) not in getfromdb('uid','transactions','tid')):
            total=total*0.9
            oid=transaction(session['cart'],session['user'],total)

            if(type(oid) is dict):
               flash(f'The item {oid[-1]} has exceeded the available quantity of {oid[0]}',category='alert-message')
               k=session['cart']
               k.pop(oid[1])
               session['cart']=k
               return redirect(url_for('cart_page'))
            
            
            if(oid!=None):
             session.pop('cart')
             session.pop('_flashes', None) 
             flash(f'Your order has been placed with order ID {oid} with total amount {total} with coupon ', 'normal-message')  
         else:
            oid=transaction(session['cart'],session['user'],total)
            if(type(oid) is dict):
               flash(f'The item {oid[-1]} has exceeded the available quantity of {oid[0]}',category='alert-message')
               k=session['cart']
               k.pop(oid[1])
               session['cart']=k
               return redirect(url_for('cart_page'))
            if(oid!=None):
             session.pop('cart')
             session.pop('_flashes', None)  
             flash(f'Your order has been placed with order ID {oid} with total amount {total} ', 'normal-message')   
       
         return redirect(url_for('shop_page'))
        except:
           
            flash(f'Add some items in the cart', 'alert-message')
        
        return redirect(url_for('shop_page'))
         


       

        
@app.route('/search',methods=['GET','POST'])
def search_page():
    
    if request.method == 'POST':
         
         catlist=getfromdb_as_dict('*','category','c_id')
         catlist1={}

         for ele in catlist:
             catlist1[ele['category_name']]=ele['c_id']

         catlist2=[]
         categories=[]
         search=""

         for ele in catlist1.keys():
             catlist2.append(ele)
        
         
         for key in request.form.keys():
             if(key=='search' and request.form[key]!=""):
                 search=request.form[key]
             elif(key!='search' and key in catlist2):
                 categories.append(catlist1[key])

         final_prod=[]

         if(categories==[]):
          p=getfromdb_as_dict('*','items','iid')
          q=[]
          for ele in p:         
            newele=ele
            newele['image']=get_image_for_item(ele['i_id'])
            q.append(newele)
         elif(categories!=[]):
          q=[]
          
          for elem in categories:            
            c_id=(elem)
            p=getfromdbwhere_as_dict('*','items','iid',f'c_id={c_id}')
           
            for ele in p:         
                newele=ele
                newele['image']=get_image_for_item(ele['i_id'])
                q.append(newele)

         if(search==""):
             final_prod=q
         else:
             for item in q:
                 search=search.strip('')
                 if(search in item['Name'] or search in item['description'] or search in item['tags']):
                     final_prod.append(item)


       
         return render_template('search.html',catfunc=getfromdb_as_dict('category_name','category','c_id'),products=final_prod)
    else:
        
          p=getfromdb_as_dict('*','items','iid')
          q=[]
          for ele in p:         
            newele=ele
            newele['image']=get_image_for_item(ele['i_id'])
            q.append(newele)

          
          
          return render_template('search.html',catfunc=getfromdb_as_dict('category_name','category','c_id'),products=q)       
        
        
       
        

