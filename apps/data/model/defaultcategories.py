from mongoengine import StringField, Document


class DefaultCategories(Document):
    name = StringField(required=True, unique=True)
    meta ={'collection': 'default_categories'}


