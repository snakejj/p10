from django.shortcuts import render
from products.models import Product
import random
import logging


def search_results(request):
    surrogate_search = False
    surrogates = False
    surrogates_clean = []
    try:
        if request.GET:
            logger = logging.getLogger(__name__)
            logger.info('New search', exc_info=True, extra={
                    # Optionally pass a request and we'll grab any information we can
                    'request': request,
            })

            product_searched = request.GET.get("product_searched")
            first_result = Product.objects.filter(product_name__icontains=product_searched)[0]
            surrogate_search = True
        else:
            first_result = None
    except IndexError:
        first_result = False

    if surrogate_search:

        surrogates_raw = Product.objects.filter(
            category=first_result.category,
            nutrition_grade_fr__lt=first_result.nutrition_grade_fr
        )
        if surrogates_raw:
            for product in surrogates_raw:
                surrogates_clean.append(product)

            random.shuffle(surrogates_clean)
            surrogates = surrogates_clean[:6]

    return render(request, 'search/resultats.html', {
        'title': "Page de resultats",
        'product_found': first_result,
        'surrogates': surrogates,
    })
