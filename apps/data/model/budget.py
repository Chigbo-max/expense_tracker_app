from datetime import datetime

from mongoengine import Document, FloatField, StringField, ReferenceField, IntField, BooleanField, DateTimeField

from apps.data.model.user import User


class Budget(Document):
    user = ReferenceField(User, required=True)
    category = StringField(required=True)
    limit = FloatField(required=True)
    current_spending = FloatField(default=0.0)
    month = IntField(min_value=1, max_value=12)
    year = IntField(required=True)
    rollover_enabled = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now)
    last_updated = DateTimeField(default=datetime.now)


    meta ={
        'indexes': [

                {'fields':['user', 'category','month', 'year'],
                 'unique':True,
                 'name': 'Unique budget per month',},
                {'fields': ['user', 'rollover_enabled'],
                 'name': 'Rollover index',},

        ]
    }
