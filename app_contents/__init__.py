from flask import Flask, render_template, redirect, session,request,url_for,flash, get_flashed_messages
from datetime import timedelta



app=Flask(__name__)
app.config['SECRET_KEY'] = '65425b99692dc442ec36170e460a4987f94b9849b3154afe'

app.permanent_session_lifetime=timedelta(minutes=15)



from app_contents import routes_user
from app_contents import routes_manager
from app_contents import routes_market
