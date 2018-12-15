#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Donnerstag 13. Dezember 2018
@author: akurm
"""

from flask import render_template, url_for, redirect, flash, session, request
from app import app, db
from app.forms import ScanForm, MediaAddForm
from app.models import Reader, Media
import hashlib, os
from app.Bacode128Generator import Barcode128


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
	form = ScanForm()

	if form.validate_on_submit():
		barcode = form.barcode.data

		hex_id = barcode[1:]

		if barcode[:1] == "L":
			reader_id = int(hex_id, 16)
			return redirect(url_for('reader', reader_id=reader_id))

		if barcode[:1] == "M":
			media_id = int(hex_id, 16)
			return redirect(url_for('media', media_id=media_id))

		flash(u'Barcode wurde nicht erkannt.', 'danger')
		return redirect(url_for('index'))

	media_count = Media.query.count()
	reader_count = Reader.query.count()
	loaned_count = Media.query.filter(Media.reader_id > 0).count()
	in_stock_count = media_count - loaned_count

	reader_with_loaned = Reader.query.filter(Reader.media_loaned.any() > 0).count()
	reader_without_loaned = reader_count - reader_with_loaned


	return render_template(
						'index.html',
						title='Startseite',
						form=form,
						media_count=media_count,
						reader_count=reader_count,
						in_stock_count=in_stock_count,
						loaned_count=loaned_count,
						reader_with_loaned=reader_with_loaned,
						reader_without_loaned=reader_without_loaned)


@app.route('/reader/<reader_id>', methods=['GET', 'POST'])
def reader(reader_id):
	reader = Reader.query.filter_by(id=reader_id).first()

	if not reader is None:

		# hex wert bestimmen
		hex_id = 'L' + hex(reader.id)

		# barcode generieren
		basedir = os.path.abspath(os.path.dirname(__file__))
		barcode = Barcode128(hex_id, reader.first_name + ", " + reader.last_name)
		barcode.save(basedir + "/static/reader_barcodes/" + hex_id)

		return render_template(
			'reader.html',
			title=reader.first_name+', '+reader.last_name,
			reader=reader, hex_id=hex_id
		)
	else:
		flash(u'Leser wurde nicht in der Datenbank gefunden.', 'danger')
		return redirect(url_for('index'))


@app.route('/media/<media_id>', methods=['GET', 'POST'])
def media(media_id):
	form = ScanForm()

	media = Media.query.filter_by(id=media_id).first()

	# wurde ein reader zum ausleihen gescannt?
	if form.validate_on_submit():
		barcode = form.barcode.data
		hex_id = barcode[1:]
		if barcode[:1] == "L":
			reader_id = int(hex_id, 16)
			media.reader_id = reader_id
			db.session.commit()
			return redirect(url_for('media', media_id=media_id))
		else:
			flash('Die ist kein gültiger Barcode einer Leserin oder eines Lesers.', 'danger')
			return redirect(url_for('media', media_id=media_id))

	if not media is None:

		# hex wert bestimmen
		hex_id = 'M' + hex(media.id)

		# barcode generieren
		basedir = os.path.abspath(os.path.dirname(__file__))
		barcode = Barcode128(hex_id, 'Schulbücherei Asselbachschule')
		barcode.save(basedir + "/static/media_barcodes/" + hex_id)




		return render_template(
			'media.html',
			title=media.title,
			media=media, hex_id=hex_id,
			form=form
		)
	else:
		flash(u'Medium wurde nicht in der Datenbank gefunden.', 'danger')
		return redirect(url_for('index'))


@app.route('/media_back/<media_id>')
def media_back(media_id):
	media = Media.query.filter_by(id=media_id).first()
	reader_id = media.reader_id
	media.reader_id = None
	db.session.commit()
	flash(u'Medium: "' + media.title + u'" wurde zurückgegeben.', 'success')
	return redirect(url_for('reader', reader_id=reader_id))


@app.route('/media_add', methods=['GET', 'POST'])
def media_add():
	form = MediaAddForm()

	if form.validate_on_submit():
		media = Media(title=form.title.data, author=form.author.data)
		db.session.add(media)
		db.session.commit()
		flash(u'Medium "' + media.title + '" wurde hinzugefügt.', 'success')
		return redirect(url_for('index'))

	return render_template('media_add.html', title='Medium hinzufügen', form=form)