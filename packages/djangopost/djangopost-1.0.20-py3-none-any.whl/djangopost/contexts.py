from djangopost.models import CategoryModel


def CategoryUniversalContext(request):
    djangopost_category = CategoryModel.objects.published()
    return {"djangopost_category": djangopost_category}
