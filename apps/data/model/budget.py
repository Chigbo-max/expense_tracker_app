from mongoengine import Document, FloatField, StringField, ReferenceField, IntField

from apps.data.model.user import User


class Budget(Document):
    user = ReferenceField(User, required=True)
    category = StringField(required=True)
    limit = FloatField(required=True)
    month = IntField(required=True)
    year = IntField(required=True)
