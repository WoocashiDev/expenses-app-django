from collections import OrderedDict

from django.db.models import Sum, Value
from django.db.models.functions import Coalesce, ExtractMonth, ExtractYear



def summary_per_category(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(category_name=Coalesce('category__name', Value('-')))
        .order_by()
        .values('category_name')
        .annotate(s=Sum('amount'))
        .values_list('category_name', 's')
    ))

def summary_per_period(queryset):
    periods = queryset.annotate(
            month=ExtractMonth('date'),
            year=ExtractYear('date'),
            ).order_by('-year').values('year','month').annotate(total=Sum('amount')).values('year', 'month', 'total')
    return periods
    

