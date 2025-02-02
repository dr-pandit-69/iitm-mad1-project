from flask import Flask, jsonify,request
from app_contents.functions import *
from app_contents import app
from flask_restful import Api, Resource, reqparse
import random
from app_contents import session



api=Api(app)


class CategoryResource(Resource):
    def get(self):
        categories = getfromdb_as_dict('c_id, category_name', 'category', 'c_id')
        return {'categories': categories}

class ProductHomeResource(Resource):
    def get(self):
            
   
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
        
        
        return products



class AddToCart(Resource):
    def post(self):
       flag=True
       
       try:
        if(session["user"]==None):
            return {'message': 'Please login to add items to the cart', 'redirect': 'login_page'}, 401
       except KeyError:
            return {'message': 'Please login to add items to the cart', 'redirect': 'login_page'}, 401
        
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
         flag=False
        
         return {'message': 'Enter a quantity lower than {existing_qty-q}', 'redirect': '/shop_page'}, 401
        
       if item_id in cart.keys() and flag:
            cart[item_id]=int(cart[item_id])+quantity 
            
       elif(flag):
        cart[item_id]=quantity   

       return {'message': 'Enter a quantity lower than {existing_qty-q}', 'redirect': '/shop_page'}, 401 
    
api.add_resource(AddToCart, '/api/add_to_cart')

api.add_resource(CategoryResource, '/api/categories')
api.add_resource(ProductHomeResource, '/api/products_home')


