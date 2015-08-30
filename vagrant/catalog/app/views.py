from app import app, session
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, jsonify
from flask import session as login_session

# functions to help with login/logout
from auth_helpers import *

# functions to help with CRUD
from helpers import *

# WTF forms
from forms import *


@app.route('/', methods=['GET'])
def index():
	'''
	Display list of categories & items
	'''
	categories = session.query(Category)
	items = session.query(Item).order_by(Item.id.desc()).limit(10)
	return render_template('index.html', items=items, categories=categories)


@app.route('/login', methods=['GET'])
def login():
	'''
	Allows FB login
	'''
	state = ''.join(random.choice(string.ascii_uppercase + string.digits)
					for x in xrange(32))
	login_session['state'] = state
	return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
	'''
	endpoint for ajax call
	'''
	fb_login()
	return redirect('/')


@app.route('/logout')
def logout():
	'''
	Allows FB logout
	'''
	disconnect()
	return redirect('/')


@app.route('/<category_name>/items')
def category(category_name):
	'''
	provides list of items associated to a category
	'''
	category = session.query(Category).filter_by(name=category_name).one()
	items = session.query(Item).filter_by(category_id=category.id)
	return render_template('category.html', category=category, items=items)


@app.route('/addItem', methods=['GET', 'POST'])
def addItem():
	'''
	Form to add new items
	'''
	form = addItemForm()
	categories = session.query(Category)
	if request.method == 'POST' and form.validate():
		# check if an item with parsed name already exists
		name = session.query(Item).filter_by(name=form.name.data).first()
		if name != None:
			flash("An item with that name already exists", 'error')
			return render_template('additem.html', user=login_session, form=form, categories=categories)
		flash("Item added", 'success')
		createItem(form)
		return redirect('/')
	else:
		return render_template('additem.html', user=login_session, form=form, categories=categories)


@app.route('/<category_name>/<item_name>/', methods=['GET'])
def viewItem(item_name, category_name):
	item = session.query(Item).filter_by(name=item_name).first()
	return render_template('item.html', item=item)


@app.route('/<category_name>/<item_name>/edit/', methods=['GET', 'POST'])
def editItem(item_name, category_name):
	'''
	Form to add edit items, only allows creator to edit
	'''
	form = addItemForm()
	categories = session.query(Category)
	item = session.query(Item).filter_by(name=item_name).first()
	category = session.query(Category).filter_by(name=category_name).first()

	# check if user has permission
	if login_session['user_id'] != item.user_id:
		flash("You do not have permissions to edit this item", 'error')
		return redirect('/')

	if request.method == 'POST' and form.validate():
		# add new info to item
		updateItem(form, item)
		flash("Item updated!", 'success')
		return redirect('/')
	else:
		return render_template('edititem.html', item=item, form=form, category=category, categories=categories)


@app.route('/<category_name>/<item_name>/delete/', methods=['GET', 'POST'])
def deleteItem(item_name, category_name):
	'''
	Deletes item, only allows creator to delete
	'''
	item = session.query(Item).filter_by(name=item_name).one()

	# check if user has permission
	if login_session['user_id'] != item.user_id:
		flash("You do not have permissions to edit this item", 'error')
		return redirect('/')

	if request.method == 'POST':
		session.delete(item)
		session.commit()
		category = session.query(Category).filter_by(
			name=category_name).first()
		itemsLeft = session.query(Item).filter_by(category=category).first()
		# if there are no more items in category delete it.
		if itemsLeft == None:
			session.delete(category)
			session.commit()

		flash("menu item deleted!", 'success')
		return redirect('/')
	else:
		return render_template(
			'deleteitem.html', item=item)


@app.route('/api', methods=['GET'])
def api():
	'''
	Index for json endpoints
	'''
	return render_template('api.html')


@app.route('/catalog.json', methods=['GET'])
def getItems():
	'''
	items json endpoint
	'''
	items = session.query(Item).all()
	return jsonify(items=[i.serialize for i in items])


@app.route('/categories.json', methods=['GET'])
def getCategories():
	'''
	categories json endpoint
	'''
	categories = session.query(Category).all()
	return jsonify(categories=[c.serialize for c in categories])


@app.route('/users.json', methods=['GET'])
def getUsers():
	'''
	users json endpoint
	'''
	users = session.query(User).all()
	return jsonify(users=[u.serialize for u in users])
