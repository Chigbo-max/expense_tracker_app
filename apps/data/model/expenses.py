from datetime import datetime

from mongoengine import Document, ReferenceField, FloatField, StringField, DateTimeField

from apps.data.model.user import User


class Expenses(Document):
    user = ReferenceField(User, required=True)
    amount = FloatField(required=True)
    category = StringField(required=True)
    merchant = StringField()
    recipient = StringField()
    description = StringField(required=True)
    date = DateTimeField(default= datetime.now, required=True)