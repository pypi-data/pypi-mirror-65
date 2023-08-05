from djangoarticle.models import CategoryModelScheme


def CategoryUniversalContext(request):
    djangoarticle_category = CategoryModelScheme.objects.published()
    return {"djangoarticle_category": djangoarticle_category}