#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Donnerstag 13. Dezember 2018
@author: akurm
"""

from flask import render_template, url_for, redirect, flash, session, request
from app import app
from app.forms import ScanForm
from app.models import Reader, Book


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
	form = ScanForm()

	if form.validate_on_submit():
		return redirect(url_for('reader', reader_id=form.barcode.data))

	book_count = Book.query.count()
	reader_count = Reader.query.count()
	in_stock_count = 0
	loaned_count = 0
	reader_with_loaned = 0
	reader_without_loaned = 0


	return render_template(
						'index.html',
						title='Startseite',
						form=form,
						book_count=book_count,
						reader_count=reader_count,
						in_stock_count=in_stock_count,
						loaned_count=loaned_count,
						reader_with_loaned=reader_with_loaned,
						reader_without_loaned=reader_without_loaned)


@app.route('/reader/<reader_id>', methods=['GET', 'POST'])
def reader(reader_id):
	reader = Reader.query.filter_by(id=reader_id).first()
	if not reader is None:
		return render_template('reader.html', title='Leser', reader=reader)
	else:
		flash(u'Leser wurde nicht in der Datenbank gefunden.', 'danger')
		return redirect(url_for('index'))