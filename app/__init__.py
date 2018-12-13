#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Donnerstag 13. Dezember 2018
@author: akurm
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
#from flask_session import Session

app = Flask(__name__)
app.config.from_object(Config)

#Session(app)

db = SQLAlchemy(app)

from app import routes, models