from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
import config #our super sweet configuration module!
from datetime import datetime

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from db_setup import Base

app = Flask(__name__)

__cfg = config.getConfig() #Are we running locally, in production? In Testing? This object will manage configuration!
app.config.from_object(__cfg) 
app.configType = __cfg

print "Initialized with config:%s" % __cfg

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

from app import views