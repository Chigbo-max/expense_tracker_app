from datetime import datetime

from mongoengine import Document, ReferenceField, StringField, DateTimeField

from apps.data.model.user import User


class Notifications(Document):
    user = ReferenceField(User, required=True)
    title = StringField(required=True)
    message = StringField(required=True)
    category = StringField(required=True)
    created_at = DateTimeField(default=datetime.now)
    meta={'collection': 'notifications'}
