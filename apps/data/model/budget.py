from mongoengine import Document, FloatField, StringField, ReferenceField, IntField

from apps.data.model.user import User


class Budget(Document):
    user = ReferenceField(User, required=True)
    category = StringField(required=True)
    limit = FloatField(required=True)
    month = IntField(min_value=1, max_value=12)
    year = IntField(required=True)
    rollover_amount = FloatField(default=0)
