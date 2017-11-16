#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from flask import Flask, request, redirect, render_template, url_for
#from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import datetime
from flask import Flask,session, request, flash, url_for, redirect, render_template, abort, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.login import login_user , logout_user , current_user , login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug import secure_filename
import os

app = Flask(__name__)
app.config.from_pyfile('fxlovely.cfg')
db = SQLAlchemy(app)

ALLOWED_EXTENSIONS = set(['png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG', 'gif', 'GIF', 'bmp', 'BMP', 'mp4', 'MP4', 'mov', 'MOV'])
ALLOWED_EXTENSIONS_V = set(['mp4', 'MP4', 'mov', 'MOV'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def allowed_file_v(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS_V


login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'

class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id',db.Integer , primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(250))
    registered_on = db.Column('registered_on' , db.DateTime)
    news = db.relationship('News' , backref='user',lazy='dynamic')
    videos = db.relationship('Videos' , backref='user',lazy='dynamic')
    products = db.relationship('Products', backref='user', lazy='dynamic')
    sales = db.relationship('Sales', backref='user', lazy='dynamic')
    customer = db.relationship('Customer', backref='user', lazy='dynamic')


    def __init__(self , username , password):
        self.username = username
        self.set_password(password)
        self.registered_on = datetime.utcnow()

    def set_password(self , password):
        self.password = generate_password_hash(password)

    def check_password(self , password):
        return check_password_hash(self.password , password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column('products_id', db.Integer, primary_key=True)
    item = db.Column(db.String(60))
    title = db.Column(db.String(60))
    text = db.Column(db.String)
    pic1 = db.Column(db.String)
    pub_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __init__(self, title, text):
        self.item = None
        self.title = title
        self.text = text
        self.pic1 = None
        self.pub_date = datetime.utcnow()

class Sales(db.Model):
    __tablename__ = 'sales'
    id = db.Column('sales_id', db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.Integer)
    text = db.Column(db.String)
    pic1 = db.Column(db.String)
    pic2 = db.Column(db.String)
    pic3 = db.Column(db.String)
    pub_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __init__(self, title, text):
        self.title = title
        self.year = None
        self.text = text
        self.pic1 = None
        self.pic2 = None
        self.pic3 = None
        self.pub_date = datetime.utcnow()

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column('news_id', db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    text = db.Column(db.String)
    pic1 = db.Column(db.String)
    pic2 = db.Column(db.String)
    pic3 = db.Column(db.String)
    pub_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.pic1 = None
        self.pic2 = None
        self.pic3 = None
        self.pub_date = datetime.utcnow()
        
class Videos(db.Model):
    __tablename__ = 'videos'
    id = db.Column('videos_id', db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    text = db.Column(db.String)
    vid1 = db.Column(db.String)
    vid2 = db.Column(db.String)
    vid3 = db.Column(db.String)
    pub_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.vid1 = None
        self.vid2 = None
        self.vid3 = None
        self.pub_date = datetime.utcnow()

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column('customer_id', db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    text = db.Column(db.String)
    pic1 = db.Column(db.String)
    pic2 = db.Column(db.String)
    pic3 = db.Column(db.String)
    pub_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.pic1 = None
        self.pic2 = None
        self.pic3 = None
        self.pub_date = datetime.utcnow()
        
class Messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column('messages_id', db.Integer, primary_key=True)
    inputName = db.Column(db.String(60))
    inputPhone = db.Column(db.String(60))
    inputEmail = db.Column(db.String)
    inputText = db.Column(db.String)
    pub_date = db.Column(db.DateTime)


    def __init__(self, inputName, inputPhone):
        self.inputName = inputName
        self.inputPhone = inputPhone
        self.inputEmail = None
        self.inputText = None
        self.pub_date = datetime.utcnow()

db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/news_videos')
def news():
    return render_template('news.html',
	newsx = News.query.order_by(News.pub_date.desc()).all(),
	videosx = Videos.query.order_by(Videos.pub_date.desc()).all())

@app.route('/news/<int:news_id>')
def news_detail(news_id):
    return render_template('news_detail.html',
	news1 = News.query.order_by(News.pub_date.desc()).all(),
	news2 = News.query.get(news_id))
  
@app.route('/videos/<int:videos_id>')
def videos_detail(videos_id):
    return render_template('videos_detail.html',
	videos1 = Videos.query.order_by(Videos.pub_date.desc()).all(),
	videos2 = Videos.query.get(videos_id))

@app.route('/products')
def products():
    productsx = Products.query.order_by(Products.id).all()
    return render_template('products.html', productsx = productsx, page_id = 1 )

@app.route('/products/page/<int:page_id>')
def products_page(page_id):
    productsx = Products.query.order_by(Products.id).all()
    return render_template('products.html', productsx = productsx, page_id = page_id)
  
@app.route('/products/<int:products_id>')
def products_detail(products_id):
    return render_template('products_detail.html',
	products1 = Products.query.order_by(Products.id).all(),
	products2 = Products.query.get(products_id))

@app.route('/sales')
def sales():
    year_id = 2015
    page_id = 1
    salesx = Sales.query.filter_by(year = year_id).order_by(Sales.id).all()
    customerx = Customer.query.order_by(Customer.pub_date.desc()).all()
    return render_template('sales.html', salesx = salesx, customerx = customerx, page_id = page_id, year_id = year_id)

@app.route('/sales/<int:year_id>/<int:page_id>')
def sales_year_page(year_id, page_id):
    salesx = Sales.query.filter_by(year = year_id).order_by(Sales.id).all()
    customerx = Customer.query.order_by(Customer.pub_date.desc()).all()
    return render_template('sales.html', salesx = salesx, customerx = customerx, year_id = year_id, page_id = page_id)
  
@app.route('/sales/<int:sales_id>')
def sales_detail(sales_id):
    return render_template('sales_detail.html',
	customerx = Customer.query.order_by(Customer.pub_date.desc()).all(),
	salesx = Sales.query.get(sales_id))

@app.route('/customer/<int:customer_id>')
def customer_detail(customer_id):
    return render_template('customer_detail.html',
	customer1 = Customer.query.order_by(Customer.pub_date.desc()).all(),
	customer2 = Customer.query.get(customer_id))

@app.route('/hr')
def hr():
    return render_template('hr.html')

@app.route('/contact', methods = ['GET', 'POST'])
def contact():
    if request.method == 'POST':
	messagesx = Messages(request.form['inputName'], request.form['inputPhone'])
	messagesx.inputEmail = request.form['inputEmail']
	messagesx.inputText = request.form['inputText']
	db.session.add(messagesx)
	db.session.commit()
	flash('Message has been submited')
	return render_template('index.html')
    return render_template('contact.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True
    registered_user = User.query.filter_by(username=username, password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid', 'error')
        return redirect(url_for('login'))
    login_user(registered_user, remember = remember_me)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('manage'))

#@app.route('/manage', methods = ['GET', 'POST'])
#@login_required
#def manage():
    #if request.method == 'POST':
	#if not request.form['title']:
	    #flash('Title is required', 'error')
	#elif not request.form['text']:
	    #flash('Text is required', 'error')	  
	    ##file = request.files['pfile']
	    ##if not file:
		##newsx = News(request.form['title'], request.form['text'])
		##newsx.user = g.user
		##db.session.add(newsx)
		##db.session.commit()
		##flash('News without image item was successfully created')
		##return redirect(url_for('manage'))
	    ##else:
		##if allowed_file(file.filename):
		    ###filename = secure_filename(files.filename)
		    ##file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
		    ##newsx = News(request.form['title'], request.form['text'])
		    ##newsx.pic1 = '/' + app.config['UPLOAD_FOLDER'] + '/' + file.filename 
		    ##newsx.user = g.user
		    ##db.session.add(newsx)
		    ##db.session.commit()
		    ##flash('News with image item was successfully created')
		    ##return redirect(url_for('manage'))
	#else:
	    #upload_files = request.files.getlist("pfile[]")
	    #filenames = []
	    #flags = 0
	    #for file in upload_files[:3]:
		#if not file:
		    #flags = 1
		#elif allowed_file(file.filename):
		    #file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
		    #filenames.append(file.filename)
	    #if flags ==0 and len(filenames) < min(len(upload_files), 3):
		#flash('unspport file in uploading', 'error')
	    #elif flags == 1:
		#newsx = News(request.form['title'], request.form['text'])
		#newsx.user = g.user
		#db.session.add(newsx)
		#db.session.commit()
		#flash('News without image item was successfully created')
		#return redirect(url_for('manage'))
	    #elif len(filenames) == 1:
		#newsx = News(request.form['title'], request.form['text'])
		#newsx.pic1 = '/' + app.config['UPLOAD_FOLDER'] + '/' + filenames[0]
		#newsx.user = g.user
		#db.session.add(newsx)
		#db.session.commit()
		#flash('News with image item was successfully created')
		#return redirect(url_for('manage'))  
	    #elif len(filenames) == 2:
		#newsx = News(request.form['title'], request.form['text'])
		#newsx.pic1 = '/' + app.config['UPLOAD_FOLDER'] + '/' + filenames[0]
		#newsx.pic2 = '/' + app.config['UPLOAD_FOLDER'] + '/' + filenames[1]
		#newsx.user = g.user
		#db.session.add(newsx)
		#db.session.commit()
		#flash('News with image item was successfully created')
		#return redirect(url_for('manage'))
	    #elif len(filenames) == 3:
		#newsx = News(request.form['title'], request.form['text'])
		#newsx.pic1 = '/' + app.config['UPLOAD_FOLDER'] + '/' + filenames[0]
		#newsx.pic2 = '/' + app.config['UPLOAD_FOLDER'] + '/' + filenames[1]
		#newsx.pic3 = '/' + app.config['UPLOAD_FOLDER'] + '/' + filenames[2]
		#newsx.user = g.user
		#db.session.add(newsx)
		#db.session.commit()
		#flash('News with image item was successfully created')
		#return redirect(url_for('manage'))
    #return render_template('web_manage.html', 
	#newsx = News.query.filter_by(user_id = g.user.id).order_by(News.pub_date.desc()).all())
@app.route('/manage')
@login_required
def manage():
    return render_template('web_manage.html', m_idx = 0, userx = g.user.id)

@app.route('/manage/<int:m_id>',  methods = ['GET', 'POST'])
@login_required
def manage_id(m_id):
    if m_id == 1:
	if request.method == 'POST':
	    if not request.form['title']:
		flash('Title is required', 'error')
	    elif not request.form['text']:
		flash('Text is required', 'error')
		#file = request.files['pfile']
		#if not file:
		    #newsx = News(request.form['title'], request.form['text'])
		    #newsx.user = g.user
		    #db.session.add(newsx)
		    #db.session.commit()
		    #flash('News without image item was successfully created')
		    #return redirect(url_for('manage'))
		#else:
		    #if allowed_file(file.filename):
			##filename = secure_filename(files.filename)
			#file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
			#newsx = News(request.form['title'], request.form['text'])
			#newsx.pic1 = '/' + app.config['UPLOAD_FOLDER'] + '/' + file.filename 
			#newsx.user = g.user
			#db.session.add(newsx)
			#db.session.commit()
			#flash('News with image item was successfully created')
			#return redirect(url_for('manage'))
	    else:
		files = request.files['pfile']
		if not files:
		    flash('No image was uploadded', 'error')
		else:
		    if allowed_file(files.filename):
			files.save(os.path.join(app.config['UPLOAD_FOLDER'], files.filename))
			productsx = Products(request.form['title'], request.form['text'])
			productsx.item = request.form['item']
			productsx.pic1 = '/static/uploads/' + files.filename
			productsx.user = g.user
			db.session.add(productsx)
			db.session.commit()
			flash('Products with image item was successfully created')
			return redirect(url_for('manage_id', m_id = m_id))
        query = Products.query
        if g.user.id == 0:
            query = query.order_by(Products.pub_date.desc())
        else:
            query = query.filter_by(user_id = g.user.id).order_by(Products.pub_date.desc())
	return render_template('web_manage.html', productsx = query.all(), m_idx = m_id, userx = g.user.id)
    
    elif m_id == 2:
	if request.method == 'POST':
	    if not request.form['title']:
		flash('Title is required', 'error')
	    elif not request.form['text']:
		flash('Text is required', 'error')	  
		#file = request.files['pfile']
		#if not file:
		    #newsx = News(request.form['title'], request.form['text'])
		    #newsx.user = g.user
		    #db.session.add(newsx)
		    #db.session.commit()
		    #flash('News without image item was successfully created')
		    #return redirect(url_for('manage'))
		#else:
		    #if allowed_file(file.filename):
			##filename = secure_filename(files.filename)
			#file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
			#newsx = News(request.form['title'], request.form['text'])
			#newsx.pic1 = '/' + app.config['UPLOAD_FOLDER'] + '/' + file.filename 
			#newsx.user = g.user
			#db.session.add(newsx)
			#db.session.commit()
			#flash('News with image item was successfully created')
			#return redirect(url_for('manage'))
	    else:
		upload_files = request.files.getlist("pfile[]")
		filenames = []
		flags = 0
		for file in upload_files[:3]:
		    if not file:
			flags = 1
		    elif allowed_file(file.filename):
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
			filenames.append(file.filename)
		if flags ==0 and len(filenames) < min(len(upload_files), 3):
		    flash('unspport file in uploading', 'error')
		elif flags == 1:
		    salesx = Sales(request.form['title'], request.form['text'])
		    salesx.year = request.form['year']
		    salesx.user = g.user
		    db.session.add(salesx)
		    db.session.commit()
		    flash('Sales without image item was successfully created')
		    return redirect(url_for('manage_id', m_id = m_id))
		elif len(filenames) == 1:
		    salesx = Sales(request.form['title'], request.form['text'])
		    salesx.pic1 = '/static/uploads/' + filenames[0]
		    salesx.year = request.form['year']
		    salesx.user = g.user
		    db.session.add(salesx)
		    db.session.commit()
		    flash('Sales with image item was successfully created')
		    return redirect(url_for('manage_id', m_id = m_id))  
		elif len(filenames) == 2:
		    salesx = Sales(request.form['title'], request.form['text'])
		    salesx.pic1 = '/static/uploads/' + filenames[0]
		    salesx.pic2 = '/static/uploads/' + filenames[1]
		    salesx.year = request.form['year']
		    salesx.user = g.user
		    db.session.add(salesx)
		    db.session.commit()
		    flash('Sales with image item was successfully created')
		    return redirect(url_for('manage_id', m_id = m_id))
		elif len(filenames) == 3:
		    salesx = Sales(request.form['title'], request.form['text'])
		    salesx.pic1 = '/static/uploads/' + filenames[0]
		    salesx.pic2 = '/static/uploads/' + filenames[1]
		    salesx.pic3 = '/static/uploads/' + filenames[2]
		    salesx.year = request.form['year']
		    salesx.user = g.user
		    db.session.add(salesx)
		    db.session.commit()
		    flash('Sales with image item was successfully created')
		    return redirect(url_for('manage_id', m_id = m_id))
	query = Sales.query
        if g.user.id == 0:
            query = query.order_by(Sales.pub_date.desc())
        else:
            query = query.filter_by(user_id = g.user.id).order_by(Sales.pub_date.desc())
	return render_template('web_manage.html', salesx = query.all(), m_idx = m_id, userx = g.user.id)
    
    elif m_id == 3:
	if request.method == 'POST':
	    if not request.form['title']:
		flash('Title is required', 'error')
	    elif not request.form['text']:
		flash('Text is required', 'error')	  
		#file = request.files['pfile']
		#if not file:
		    #newsx = News(request.form['title'], request.form['text'])
		    #newsx.user = g.user
		    #db.session.add(newsx)
		    #db.session.commit()
		    #flash('News without image item was successfully created')
		    #return redirect(url_for('manage'))
		#else:
		    #if allowed_file(file.filename):
			##filename = secure_filename(files.filename)
			#file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
			#newsx = News(request.form['title'], request.form['text'])
			#newsx.pic1 = '/' + app.config['UPLOAD_FOLDER'] + '/' + file.filename 
			#newsx.user = g.user
			#db.session.add(newsx)
			#db.session.commit()
			#flash('News with image item was successfully created')
			#return redirect(url_for('manage'))
	    else:
		upload_files = request.files.getlist("pfile[]")
		filenames = []
		flags = 0
		for file in upload_files[:3]:
		    if not file:
			flags = 1
		    elif allowed_file(file.filename):
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
			filenames.append(file.filename)
		if flags ==0 and len(filenames) < min(len(upload_files), 3):
		    flash('unspport file in uploading', 'error')
		elif flags == 1:
		    newsx = News(request.form['title'], request.form['text'])
		    newsx.user = g.user
		    db.session.add(newsx)
		    db.session.commit()
		    flash('News without image item was successfully created')
		    return redirect(url_for('manage_id', m_id = m_id))
		elif len(filenames) == 1:
		    newsx = News(request.form['title'], request.form['text'])
		    newsx.pic1 = '/static/uploads/' + filenames[0]
		    newsx.user = g.user
		    db.session.add(newsx)
		    db.session.commit()
		    flash('News with image item was successfully created')
		    return redirect(url_for('manage_id', m_id = m_id))  
		elif len(filenames) == 2:
		    newsx = News(request.form['title'], request.form['text'])
		    newsx.pic1 = '/static/uploads/' + filenames[0]
		    newsx.pic2 = '/static/uploads/' + filenames[1]
		    newsx.user = g.user
		    db.session.add(newsx)
		    db.session.commit()
		    flash('News with image item was successfully created')
		    return redirect(url_for('manage_id', m_id = m_id))
		elif len(filenames) == 3:
		    newsx = News(request.form['title'], request.form['text'])
		    newsx.pic1 = '/static/uploads/' + filenames[0]
		    newsx.pic2 = '/static/uploads/' + filenames[1]
		    newsx.pic3 = '/static/uploads/' + filenames[2]
		    newsx.user = g.user
		    db.session.add(newsx)
		    db.session.commit()
		    flash('News with image item was successfully created')
		    return redirect(url_for('manage_id', m_id = m_id))
	query = News.query
        if g.user.id == 0:
            query = query.order_by(News.pub_date.desc())
        else:
            query = query.filter_by(user_id = g.user.id).order_by(News.pub_date.desc())
	return render_template('web_manage.html', newsx = query.all(), m_idx = m_id, userx = g.user.id)
    
    if m_id == 4:
	if request.method == 'POST':
	    if not request.form['title']:
		flash('Title is required', 'error')
	    elif not request.form['text']:
		flash('Text is required', 'error')	  
		#file = request.files['pfile']
		#if not file:
		    #newsx = News(request.form['title'], request.form['text'])
		    #newsx.user = g.user
		    #db.session.add(newsx)
		    #db.session.commit()
		    #flash('News without image item was successfully created')
		    #return redirect(url_for('manage'))
		#else:
		    #if allowed_file(file.filename):
			##filename = secure_filename(files.filename)
			#file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
			#newsx = News(request.form['title'], request.form['text'])
			#newsx.pic1 = '/' + app.config['UPLOAD_FOLDER'] + '/' + file.filename 
			#newsx.user = g.user
			#db.session.add(newsx)
			#db.session.commit()
			#flash('News with image item was successfully created')
			#return redirect(url_for('manage'))
	    else:
		upload_files = request.files.getlist("pfile[]")
		filenames = []
		flags = 0
		for file in upload_files[:3]:
		    if not file:
			flags = 1
		    elif allowed_file_v(file.filename):
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
			filenames.append(file.filename)
		if flags ==0 and len(filenames) < min(len(upload_files), 3):
		    flash('unspport file in uploading', 'error')
		elif flags == 1:
		    flash('No video was upload', 'error')
		elif len(filenames) == 1:
		    videosx = Videos(request.form['title'], request.form['text'])
		    videosx.vid1 = '/static/uploads/' + filenames[0]
		    videosx.user = g.user
		    db.session.add(videosx)
		    db.session.commit()
		    flash('Videos was successfully created')
		    return redirect(url_for('manage_id', m_id = m_id))  
		elif len(filenames) == 2:
		    videosx = Videos(request.form['title'], request.form['text'])
		    videosx.vid1 = '/static/uploads/' + filenames[0]
		    videosx.vid2 = '/static/uploads/' + filenames[1]
		    videosx.user = g.user
		    db.session.add(videosx)
		    db.session.commit()
		    flash('Videos was successfully created')
		    return redirect(url_for('manage_id', m_id = m_id))
		elif len(filenames) == 3:
		    videosx = Videos(request.form['title'], request.form['text'])
		    videosx.vid1 = '/static/uploads/' + filenames[0]
		    videosx.vid2 = '/static/uploads/' + filenames[1]
		    videosx.vid3 = '/static/uploads/' + filenames[2]
		    videosx.user = g.user
		    db.session.add(videosx)
		    db.session.commit()
		    flash('Videos was successfully created')
		    return redirect(url_for('manage_id', m_id = m_id))
	query = Videos.query
        if g.user.id == 0:
            query = query.order_by(Videos.pub_date.desc())
        else:
            query = query.filter_by(user_id = g.user.id).order_by(Videos.pub_date.desc())
	return render_template('web_manage.html', videosx = query.all(), m_idx = m_id, userx = g.user.id)
    
    elif m_id == 5:
	if request.method == 'POST':
	    if not request.form['title']:
		flash('Title is required', 'error')
	    elif not request.form['text']:
		flash('Text is required', 'error')	  
		#file = request.files['pfile']
		#if not file:
		    #newsx = News(request.form['title'], request.form['text'])
		    #newsx.user = g.user
		    #db.session.add(newsx)
		    #db.session.commit()
		    #flash('News without image item was successfully created')
		    #return redirect(url_for('manage'))
		#else:
		    #if allowed_file(file.filename):
			##filename = secure_filename(files.filename)
			#file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
			#newsx = News(request.form['title'], request.form['text'])
			#newsx.pic1 = '/' + app.config['UPLOAD_FOLDER'] + '/' + file.filename 
			#newsx.user = g.user
			#db.session.add(newsx)
			#db.session.commit()
			#flash('News with image item was successfully created')
			#return redirect(url_for('manage'))
	    else:
		upload_files = request.files.getlist("pfile[]")
		filenames = []
		flags = 0
		for file in upload_files[:3]:
		    if not file:
			flags = 1
		    elif allowed_file(file.filename):
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
			filenames.append(file.filename)
		if flags ==0 and len(filenames) < min(len(upload_files), 3):
		    flash('unspport file in uploading', 'error')
		elif flags == 1:
		    customerx = Customer(request.form['title'], request.form['text'])
		    customerx.user = g.user
		    db.session.add(customerx)
		    db.session.commit()
		    flash('Customer without image item was successfully created')
		    return redirect(url_for('manage_id', m_id = m_id))
		elif len(filenames) == 1:
		    customerx = Customer(request.form['title'], request.form['text'])
		    customerx.pic1 = '/static/uploads/' + filenames[0]
		    customerx.user = g.user
		    db.session.add(customerx)
		    db.session.commit()
		    flash('Customer with image item was successfully created')
		    return redirect(url_for('manage_id', m_id = m_id))  
		elif len(filenames) == 2:
		    customerx = Customer(request.form['title'], request.form['text'])
		    customerx.pic1 = '/static/uploads/' + filenames[0]
		    customerx.pic2 = '/static/uploads/' + filenames[1]
		    customerx.user = g.user
		    db.session.add(customerx)
		    db.session.commit()
		    flash('Customer with image item was successfully created')
		    return redirect(url_for('manage_id', m_id = m_id))
		elif len(filenames) == 3:
		    customerx = Customer(request.form['title'], request.form['text'])
		    customerx.pic1 = '/static/uploads/' + filenames[0]
		    customerx.pic2 = '/static/uploads/' + filenames[1]
		    customerx.pic3 = '/static/uploads/' + filenames[2]
		    customerx.user = g.user
		    db.session.add(customerx)
		    db.session.commit()
		    flash('Customer with image item was successfully created')
		    return redirect(url_for('manage_id', m_id = m_id))
	query = Customer.query
        if g.user.id == 0:
            query = query.order_by(Customer.pub_date.desc())
        else:
            query = query.filter_by(user_id = g.user.id).order_by(Customer.pub_date.desc())
	return render_template('web_manage.html', customerx = query.all(), m_idx = m_id, userx = g.user.id)
    elif m_id == 6:
	return render_template('web_manage.html', 
	    messagesx = Messages.query.order_by(Messages.pub_date.desc()).all(), m_idx = m_id, userx = g.user.id)
    else:
	flash('ilega', 'error')

@app.route('/products/delete/<int:products_id>')
def delete_products(products_id):
    products_d = Products.query.get(products_id)
    db.session.delete(products_d)
    db.session.commit()
    flash('One product had been deleted')
    return redirect(url_for('manage_id', m_id = 1))

@app.route('/sales/delete/<int:sales_id>')
def delete_sales(sales_id):
    sales_d = Sales.query.get(sales_id)
    db.session.delete(sales_d)
    db.session.commit()
    flash('One sales had been deleted')
    return redirect(url_for('manage_id', m_id = 2))

@app.route('/news/delete/<int:news_id>')
def delete_news(news_id):
    news_d = News.query.get(news_id)
    db.session.delete(news_d)
    db.session.commit()
    flash('One news had been deleted')
    return redirect(url_for('manage_id', m_id = 3))

@app.route('/videos/delete/<int:videos_id>')
def delete_videos(videos_id):
    videos_d = Videos.query.get(videos_id)
    db.session.delete(videos_d)
    db.session.commit()
    flash('One videos had been deleted')
    return redirect(url_for('manage', m_id = 4))
  
@app.route('/customer/delete/<int:customer_id>')
def delete_customer(customer_id):
    customer_d = Customer.query.get(customer_id)
    db.session.delete(customer_d)
    db.session.commit()
    flash('One customer had been deleted')
    return redirect(url_for('manage', m_id = 5))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    
if __name__ == '__main__':
    app.run(debug = True)