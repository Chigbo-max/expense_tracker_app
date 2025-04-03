from apps.data.model.defaultcategories import DefaultCategories

DEFAULT_CATEGORIES =[
    {
        "name": "Transport"
    },

    {
        "name": "Housing"
    },

    {
        "name": "Food"
    },

    {
        "name": "Utilities"
    }
]

if DefaultCategories.objects.count() == 0:
    for category in DEFAULT_CATEGORIES:
        DefaultCategories(**category).save()

        # DefaultCateggories(name="Transport").save()