import datetime
from flask import url_for
from hackjack import db

class Player(db.EmbeddedDocument):
    display_name = db.StringField(max_length=255, required=True)
    passphrase = db.StringField(max_length=255, required=True)
    money = db.IntField(min_value=0, max_value=1000)
    cards = db.ListField(db.StringField(max_length=2))

class Table(db.Document):
    tableNum = db.IntField()
    players = db.ListField(db.EmbeddedDocumentField('Player'))
    turn = db.EmbeddedDocumentField('Player')
    curStart = db.IntField(min_value=1, max_value=5)

class Comment(db.EmbeddedDocument):
    content = db.StringField()

class Post(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True)
    body = db.StringField(required=True)
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))
    #comments = db.EmbeddedDocumentField('Comment')

    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug'],
        'ordering': ['-created_at']
    }

