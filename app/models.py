#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Donnerstag 13.Dezember 2018
@author: akurm
"""

from app import db


class Reader(db.Model):
    __tablename__ = 'reader'
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(64), index=True)
    first_name = db.Column(db.String(64), index=True)
    media_loaned = db.relationship('Media', backref='reader')

class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    subtitle = db.Column(db.String(64), index=True)
    author = db.Column(db.String(64), index=True)
    reader_id = db.Column(db.Integer, db.ForeignKey('reader.id'))