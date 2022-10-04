from django import forms
from .models import Expense, Category


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
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['categories'] = forms.TypedMultipleChoiceField(choices=((category.id, category.name) for category in Category.objects.all()), required=False)
