from django.views.generic.list import ListView

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, summary_per_period
from datetime import date
from django.db.models import Count
import re


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            # getting today's date
            today = date.today()
            # getting values from from_date and to_date in input fields
            from_date = form['from_date'].value()
            to_date = form['to_date'].value()

            # getting value of categories
            categories = form.cleaned_data.get('categories', '')

            # getting value of ordering_by
            ordering_by = form['ordering_by'].value()
            
            if categories:
                categories=categories
                print(categories)
            else:
                categories = Category.objects.all()

            # if there is a date chosen - keep it; else select the earliest date in the db
            if from_date:
                from_date = from_date
            else:
                from_date = Expense.objects.exclude(date__isnull=True).order_by('date').first().date
                print(from_date)

            # if there is a date chosen - keep it; else select today's date
            if to_date:
                to_date = to_date
            else:
                to_date = today
            
            if name or from_date or to_date:
                queryset = queryset.filter(
                    name__icontains=name, date__range=[
                    from_date,
                    to_date
                    ],
                    category__in = categories
                )
            
            # ordering queryset if applicable
            if ordering_by:
                queryset = queryset.order_by(ordering_by)
                print(queryset)

            # subtotal value - value as per search results
            subtotal_value = sum([expense.amount for expense in queryset])

            # total value - value as per all registered expenses
            total_value = sum([expense.amount for expense in Expense.objects.all()])


        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            summary_per_period=summary_per_period(queryset),
            subtotal_value=subtotal_value,
            total_value=total_value,
            **kwargs
            )
            
    # fixing issues with pagination and filtering
    def setup(self, request, *args, **kwargs) -> None:
        request.GET.get("page")
        request.META["QUERY_STRING"] = re.sub("(&|\?)page=(.)*", "", request.META.get("QUERY_STRING", ""))
        return super().setup(request, *args, **kwargs)

class CategoryListView(ListView):
    model = Category
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        queryset = queryset.annotate(items_count=Count('expense__category'))

        return super().get_context_data(   
                object_list=queryset
                )