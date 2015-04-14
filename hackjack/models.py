import datetime
from flask import url_for
from hackjack import db

class Player(db.EmbeddedDocument):
    display_name = db.StringField(max_length=255, required=True)
    money = db.IntField(min_value=0, max_value=1000, required=True)
    cards = db.ListField(db.StringField(max_length=2), required=True)
    status = db.StringField(required=True)
    bet = db.IntField(required=True)
    doubled_down=db.BooleanField(required=True)

class Table(db.Document):
    table_name = db.StringField(max_length=15, required=True)
    table_status = db.StringField(required=True)
    players = db.ListField(db.EmbeddedDocumentField('Player', required=True), required=True)
    turn_index = db.IntField(min_value=1, required=True)
    turn_name = db.StringField(required=True)
    curStart = db.IntField(min_value=1, max_value=5)

class Dealer(db.EmbeddedDocument):
    cards=db.ListField(db.StringField(max_length=2, required=True), required=True)
    status=db.StringField(required=True)

class User(db.Document):
    display_name = db.StringField(required=True)
    passphrase = db.StringField(required=True)

class Admin(db.Document):
    display_name = db.StringField(required=True)
    passphrase = db.StringField(required=True)

# class Post(db.Document):
#     created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
#     title = db.StringField(max_length=255, required=True)
#     slug = db.StringField(max_length=255, required=True)
#     body = db.StringField(required=True)
#     comments = db.ListField(db.EmbeddedDocumentField('Comment'))
#     #comments = db.EmbeddedDocumentField('Comment')

#     def get_absolute_url(self):
#         return url_for('post', kwargs={"slug": self.slug})

#     def __unicode__(self):
#         return self.title

#     meta = {
#         'allow_inheritance': True,
#         'indexes': ['-created_at', 'slug'],
#         'ordering': ['-created_at']
#     }

