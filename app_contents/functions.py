from os import path,getcwd, remove
import re
import sqlite3
import base64
from datetime import datetime
import io

def is_valid_email(email):
     if('@' not in email):
          return False
     if(len(email.strip('.'))<=1):
          return False
     return True

def is_valid_dob(dob):
    pattern = "^\d{2}/\d{2}/\d{4}$"
    if(dob.count('/')!=2):
        return False
    
    d=dob.split('/')
    year=int(d[-1])
    month=int(d[1])
    day=int(d[0])
   
    if(re.match(pattern,dob)==None):
        return False
       
    if(re.match(pattern,dob)!=None):
         days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year%4==0 and (year%100 != 0 or year%400==0):
        days[2] = 29
    
    return (1 <= month <= 12 and 1 <= day <= days[month])
       


def phone_num(phone_number):
   if((phone_number.count('+')<=1) and (phone_number.strip('+').isnumeric()) and (9<=len(phone_number)<=12)):
    return False
   else:
     return True


def name_validate(name):
    
    
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if(len(name)<=2):
        return 'length'
    for charac in name:
        if(charac.isnumeric()==True):
            
            return "numb"
        if(regex.search(name) != None):
            return "special"


    return True   

        
    



def is_valid_pwd(password):
    f1=False
    f2=False
    f3=False
    if(len(password)<8):
        return 'length'
    for charac in password:
        if(charac.isupper()==True):
            f1=True
        if(charac.islower()==True):
            f2=True
        if(charac.isnumeric()==True):
            f3=True    
        if(f1==True and f1==f2 and f1==f3):
            break        
     
    if(f1==False):
        return 'uppercase'
    if(f2==False):
        return 'lowercase'
    if(f3==False):
        return 'number'
    if(not(any(not charac.isalnum() for charac in password))):
        return 'special'
    
    return True



def getfromdb(columns,table,id):   

     p_db=path.join((getcwd()),'database.db')
     con = sqlite3.connect(p_db,check_same_thread=False)
     c=con.cursor()
   
     c.execute(f'SELECT {columns} FROM {table} ORDER BY {id} ASC')
    
     k=columns.count(',')
     l=[]
     m=c.fetchall()
     for ele in m:
          if(k==0 and columns!='*'):
           l.append(ele[0])
          else:
              z=list(ele)
              l.append(z)
     con.close()
  
     return l


def getfromdbwhere(columns,table,id,where):
     p_db=path.join((getcwd()),'database.db')
     con = sqlite3.connect(p_db,check_same_thread=False)
     c=con.cursor()
   
     c.execute(f'SELECT {columns} FROM {table} WHERE {where} ORDER BY {id} ASC')
      
     k=columns.count(',')
     l=[]
     m=c.fetchall()
     for ele in m:
          if(k==0 and columns!='*'):
           l.append(ele[0])
          else:
              z=list(ele)
              l.append(z)
     con.close()
  
     return l   

def getfromdb_as_dict(columns, table, id):
    p_db = path.join(getcwd(), 'database.db')
    con = sqlite3.connect(p_db, check_same_thread=False)
    c = con.cursor()

    c.execute(f'SELECT {columns} FROM {table} ORDER BY {id} ASC')
    results = c.fetchall()

    column_names = [description[0] for description in c.description]

    result_dicts = []
    for row in results:
        result_dict = {column_names[i]: row[i] for i in range(len(column_names))}
        result_dicts.append(result_dict)

    con.close()
    return result_dicts

def getfromdbwhere_as_dict(columns, table, id, where):
    p_db = path.join(getcwd(), 'database.db')
    con = sqlite3.connect(p_db, check_same_thread=False)
    c = con.cursor()

    c.execute(f'SELECT {columns} FROM {table} WHERE {where} ORDER BY {id} ASC')
    results = c.fetchall()

    column_names = [description[0] for description in c.description]

    result_dicts = []
    for row in results:
        result_dict = {column_names[i]: row[i] for i in range(len(column_names))}
        result_dicts.append(result_dict)

    con.close()
    return result_dicts

def getfromdbwhere_as_dict1(id):
    p_db = path.join(getcwd(), 'database.db')
    con = sqlite3.connect(p_db, check_same_thread=False)
    c = con.cursor()

    c.execute(f'SELECT * FROM Items WHERE i_id={id} ORDER BY i_id ASC')
    results = c.fetchall()

    column_names = [description[0] for description in c.description]

    result_dicts = []
    for row in results:
        result_dict = {column_names[i]: row[i] for i in range(len(column_names))}
        result_dicts.append(result_dict)

    con.close()
    return result_dicts[0]


def insert2db(tup,table,id_name):
     uid_new=getfromdb(id_name,'users',id_name)[-1]+1
     p_db=path.join((getcwd()),'database.db')
     con = sqlite3.connect(p_db,check_same_thread=False)
     c=con.cursor()
     tup.insert(0,uid_new)
     c.execute((f"INSERT INTO {table} VALUES {tuple(tup)}"))
     con.commit()
     con.close()

def insert2db1(tup,table,id_name):
     mid_new=getfromdb(id_name,'manager',id_name)[-1]+1
     p_db=path.join((getcwd()),'database.db')
     con = sqlite3.connect(p_db,check_same_thread=False)
     c=con.cursor()
     tup.insert(0,mid_new)
     c.execute((f"INSERT INTO {table} VALUES {tuple(tup)}"))
     con.commit()
     con.close()     

def update(d,table,id_name,id_no):
     
     p_db=path.join((getcwd()),'database.db')
     con = sqlite3.connect(p_db,check_same_thread=False)
     c=con.cursor()
     for ele in d.keys():
          c.execute((f"UPDATE {table} SET {ele} = '{d[ele]}' WHERE {id_name} = {id_no}"))
          
     con.commit()

     con.close()
     return True

def delete_account(uid):
     p_db=path.join((getcwd()),'database.db')
     con = sqlite3.connect(p_db,check_same_thread=False)
     c=con.cursor()
 
     c.execute((f"DELETE FROM users WHERE uid={uid}"))
          
     con.commit()

     con.close()
     return True

def get_image_for_item(item_id):
    p_db = path.join(getcwd(), 'database.db')
    con = sqlite3.connect(p_db, check_same_thread=False)
    c = con.cursor()

    c.execute(f'SELECT content FROM Images WHERE i_id = ?', (item_id,))
    image_data = c.fetchone()
    
    con.close()

    if image_data:
        return base64.b64encode(image_data[0]).decode('utf-8')
    else:
        return None  

def search_products(selected_categories, min_price, max_price):
    p_db = path.join(getcwd(), 'database.db')
    con = sqlite3.connect(p_db, check_same_thread=False)
    c = con.cursor()

    
    query = "SELECT * FROM items WHERE "
    if selected_categories:
        category_conditions = " OR ".join([f'c_id={c_id}' for c_id in selected_categories])
        query += f'({category_conditions}) AND '

    if min_price:
        query += f'price >= {min_price} AND '
    if max_price:
        query += f'price <= {max_price} AND '

    query += "1"  

    c.execute(query)
    search_results = c.fetchall()

    con.close()
    return search_results



def insertcat2table(name):
     try:
      c_id_new=getfromdb('c_id','category','c_id')[-1]+1
     except:
         c_id_new=0 
     table='category'
     
     p_db=path.join((getcwd()),'database.db')
     con = sqlite3.connect(p_db,check_same_thread=False)
     c=con.cursor()
     tup=(c_id_new,name)
     c.execute((f"INSERT INTO {table} VALUES {tuple(tup)}"))
     con.commit()
     con.close()


def deletecat(c_id):
     table='category'
     
     p_db=path.join((getcwd()),'database.db')
     con = sqlite3.connect(p_db,check_same_thread=False)
     c=con.cursor()     
     c.execute((f"DELETE FROM {table} WHERE c_id={c_id} "))
     con.commit()
     con.close()


def modcat(c_id,name):
         
     p_db=path.join((getcwd()),'database.db')
     con = sqlite3.connect(p_db,check_same_thread=False)
     c=con.cursor()     
     c.execute((f"UPDATE category set category_name = '{name}' WHERE c_id={c_id}"))
     con.commit()
     con.close()



    


def transaction(cart_items,uid,total):
    
    if(uid=="manager"):
        uid=-1
    p_db=path.join((getcwd()),'database.db')
    con = sqlite3.connect(p_db,check_same_thread=False)
    c=con.cursor()

    
    for ele in cart_items.keys():
          existing_qty=getfromdbwhere('qty','items','iid',f'iid={int(ele)}')[0]
          new_qty=existing_qty-cart_items[ele]
          if(new_qty<0):
              con.close()
              item=getfromdbwhere('Name','items','iid',f'iid={int(ele)}')[0]
              return({-1:item,0:existing_qty,1:ele})
              
   
    for ele in cart_items.keys():
          existing_qty=getfromdbwhere('qty','items','iid',f'iid={int(ele)}')[0]
          new_qty=existing_qty-cart_items[ele]
          if(new_qty<0):
              new_qty=0
          c.execute((f"UPDATE items SET qty = '{new_qty}' WHERE iid = {int(ele)}"))

          
    d=str(datetime.now())
    tid_new=getfromdb('tid','transactions','tid')[-1]+1
    c.execute('INSERT INTO transactions VALUES (?,?,?,?,?) ',(tid_new,uid,d,total,str(cart_items)))
    con.commit()
    con.close()

  
    return tid_new
        
     

def insertprod2table(l1):
     table='items'
     try:
      iid_new=getfromdb('iid','Items','iid')[-1]+1
     except:
         iid_new=0 
     l=l1
     l.insert(0,iid_new)     
     i_id=insert_image_into_db(l[-1])
     if(i_id==-1):
         return False
     l.pop(-1)
     l.insert(-2,i_id) 
     p_db=path.join((getcwd()),'database.db')
     con = sqlite3.connect(p_db,check_same_thread=False)
     c=con.cursor()
     tup=tuple(l)
     print(tup)     
     c.execute((f"INSERT INTO {table} VALUES {tuple(tup)}"))
     con.commit()
     con.close()




def insert_image_into_db(image_file):
    try:
        try:
           i_id_new=getfromdb('i_id','Images','i_id')[-1]+1
        except:
            i_id_new=0
        
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()       
        image_data = image_file.read()       
        clean_image_data = io.BytesIO(image_data)       
        insert_query = "INSERT INTO Images (i_id,content) VALUES (?,?)"
        cursor.execute(insert_query, (i_id_new,clean_image_data.read()))
        connection.commit()
        cursor.close()
        connection.close()
        return i_id_new
    except Exception as e:
        print("Error:", e)
        return -1

def updateimage(image_file, i_id):
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        
       

        image_data = image_file.read()
        clean_image_data = io.BytesIO(image_data)

        update_query = "UPDATE Images SET content = ? WHERE i_id = ?"
        cursor.execute(update_query, (clean_image_data.read(), i_id))
        
        if cursor.rowcount == 0:
            print(f"No row with i_id {i_id} found for update.")
            connection.rollback() 
        else:
            connection.commit()

        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print("Error:", e)
        return False
    
def update_item_columns(iid, column_updates):
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        
        set_columns = ', '.join([f"{column} = ?" for column in column_updates.keys()])        
       
        parameter_values = tuple(column_updates.values()) + (iid,)

        update_query = f"UPDATE items SET {set_columns} WHERE iid = ?"
        cursor.execute(update_query, parameter_values)
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print("Error:", e)
        return False          
          
    
    
import sqlite3
import os

def deleteprod(iid):
    try:
        p=getfromdbwhere('i_id','items','iid',f'iid={iid}')[0]
        image_i_id=getfromdbwhere('i_id','Images','i_id',f'i_id={p}')[0]
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        
        
        if image_i_id:
                     
            
            delete_product_query = f"DELETE FROM items WHERE iid = ?"
            cursor.execute(delete_product_query, (iid,))           
           
            
            connection.commit()
            cursor.close()
            connection.close()
            
            
         
            return True
        else:
            print("Product not found.")
            return False
    except Exception as e:
        print("Error:", e)
        
        return False
