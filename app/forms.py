#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Donnerstag 13. Dezember 2018
@author: akurm
"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ScanForm(FlaskForm):
	barcode = StringField('Barcode', validators=[DataRequired()])


class MediaAddForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	author = StringField('Autor', validators=[DataRequired()])