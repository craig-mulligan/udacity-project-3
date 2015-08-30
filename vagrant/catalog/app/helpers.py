from flask import session as login_session
from app import session
from db_setup import Item, User, Category

from auth_helpers import *

def categoryCheck(form):
	'''
	Checks if parsed category name exists, if not it creates one
	'''
	category = session.query(Category).filter_by(name=form.category.data).first()
	if category == None:
		newCategory = Category(name=form.category.data, user_id=login_session['user_id'])
		session.add(newCategory)
		session.commit()
		category = session.query(Category).filter_by(name=form.category.data).first()
	return category

def getUserID(email):
	try:
		user = session.query(User).filter_by(email=email).one()
		return user.id
	except:
		return None

def createItem(form):
	category = categoryCheck(form)
	newItem = Item(name=form.name.data, description=form.description.data, category_id=category.id, user_id=login_session['user_id'])	
	session.add(newItem)
	session.commit()

def updateItem(form, item):
	item.name = form.name.data
	item.description = form.description.data
	category = categoryCheck(form)
	item.category_id = category.id
	session.commit()