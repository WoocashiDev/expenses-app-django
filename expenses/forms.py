from django import forms
from .models import Expense, Category
from django.forms import widgets


class ExpenseSearchForm(forms.ModelForm):

    ORDERING_CHOICES = (
    ('',''),
    ('date', 'By date: ascending'),
    ('-date', 'By date: descending'),
    ('category', 'By category: ascending'),
    ('-category', 'By category: descending'),
    )

    from_date = forms.DateTimeField(required=False)
    to_date = forms.DateTimeField(required=False)

    ordering_by = forms.TypedChoiceField(choices=ORDERING_CHOICES, required=False)


    class Meta:
        model = Expense
        fields = ('name','from_date','to_date', 'ordering_by')
        

    def __init__(self, *args, **kwargs):
        super(ExpenseSearchForm, self).__init__(*args, **kwargs)

        self.fields['name'].required = False

        self.fields['categories'] = forms.TypedMultipleChoiceField(choices=((category.id, category.name) for category in Category.objects.all()), required=False)

        self.labels = {'name':'Expense name', "from_date": "Search start date", "to_date": "Search end date", 'ordering_by': "Order search results", "categories": ""}

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': f'{self.labels[name]}'})

