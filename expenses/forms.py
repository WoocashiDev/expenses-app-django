from django import forms
from .models import Expense, Category

# fetching choices from the Category db
CHOICES = ((category.id, category.name) for category in Category.objects.all())

class ExpenseSearchForm(forms.ModelForm):
    from_date = forms.DateTimeField(required=False)
    to_date = forms.DateTimeField(required=False)

    # passing choices to TypedMultipleChoiceField
    categories = forms.TypedMultipleChoiceField(choices=CHOICES, required=False)
    class Meta:
        model = Expense
        fields = ('name','from_date','to_date', 'categories')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
