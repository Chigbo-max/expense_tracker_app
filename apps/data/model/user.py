from datetime import datetime

from mongoengine import Document, EmailField, StringField, DateTimeField, EnumField, ListField

from apps.data.model.status import AccountStatus


class User(Document):
    email = EmailField(required=True, unique=True)
    custom_categories = ListField(StringField())
    role=StringField(choices=['admin','user'], default='user')
    status=EnumField(AccountStatus, default=AccountStatus.ACTIVE)
    created_at = DateTimeField(default=datetime.now)
