from mongoengine import StringField, Document


class DefaultCategories(Document):
    name = StringField(required=True, unique=True)


