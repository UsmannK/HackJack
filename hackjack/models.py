import datetime
from flask import url_for
from hackjack import db

class Player(db.EmbeddedDocument):
    display_name = db.StringField(max_length=255, required=True)
    money = db.IntField(min_value=0, max_value=1000, required=True)
    cards = db.ListField(db.StringField())
    status = db.StringField(required=True)
    status_code = db.IntField(required=True)
    bet = db.IntField(required=True)
    doubled_down=db.BooleanField(required=True)

class Dealer(db.EmbeddedDocument):
    cards=db.ListField(db.StringField(max_length=2, required=True), required=True)
    flipped = db.BooleanField(required=True)

class Table(db.Document):
    table_name = db.StringField(max_length=15, required=True)
    table_admin_name = db.StringField(required=True)
    table_status_code = db.IntField(required=True)
    table_status = db.StringField(required=True)
    players = db.ListField(db.EmbeddedDocumentField('Player', required=True), required=True)
    turn_index = db.IntField(min_value=0, required=True)
    turn_name = db.StringField(required=True)
    curStart = db.IntField(min_value=0, max_value=5)
    min_bet = db.IntField(min_value=5, required=True)
    drawn_cards = db.ListField(db.StringField())
    dealer = db.EmbeddedDocumentField('Dealer')

class User(db.Document):
    display_name = db.StringField(required=True)
    passphrase = db.StringField(required=True)

class Admin(db.Document):
    display_name = db.StringField(required=True)
    passphrase = db.StringField(required=True)
