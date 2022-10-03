from django import forms
from .models import Expense, Category

# fetching choices from the Category db
CATEGORY_CHOICES = ((category.id, category.name) for category in Category.objects.all())

ORDERING_CHOICES = (
    ('',''),
    ('-date', 'By date: ascending'),
    ('date', 'By date: descending'),
    ('-category', 'By category: asceding'),
    ('category', 'By category: desceding'),
)

class ExpenseSearchForm(forms.ModelForm):
    from_date = forms.DateTimeField(required=False)
    to_date = forms.DateTimeField(required=False)

    # passing choices to TypedMultipleChoiceField
    categories = forms.TypedMultipleChoiceField(choices=CATEGORY_CHOICES, required=False)
    ordering_by = forms.TypedChoiceField(choices=ORDERING_CHOICES, required=False)


    class Meta:
        model = Expense
        fields = ('name','from_date','to_date', 'categories', 'ordering_by')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
